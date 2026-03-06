"""
DocumentProcessor Lambda Function
===================================
Triggered by S3 upload events when new documents land in raw/ folder.
Downloads the document, chunks it into 1000-token segments with 200-token
overlap, and sends each chunk to SQS for embedding generation.
"""

import json
import os
import re
import boto3
import tiktoken
from datetime import datetime

# ── Configuration ──────────────────────────────────────────
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", "200"))
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "")

# ── AWS Clients ─────────────────────────────────────────────
s3_client = boto3.client("s3")
sqs_client = boto3.client("sqs", region_name="us-east-1")

# ── Tokenizer ───────────────────────────────────────────────
# cl100k_base is the standard modern encoding
# Works well as a token estimator for Bedrock models
encoder = tiktoken.get_encoding("cl100k_base")

def chunk_document(text, source_url, title, category, scraped_at):
    """
    Split a document into overlapping chunks of CHUNK_SIZE tokens.
    Returns a list of chunk dictionaries ready for SQS.
    """
    # Encode the entire document into tokens
    tokens = encoder.encode(text)
    total_tokens = len(tokens)

    # If document is shorter than chunk size, return as single chunk
    if total_tokens <= CHUNK_SIZE:
        return [{
            "chunk_id": f"{_url_to_id(source_url)}_chunk_0",
            "content": text,
            "token_count": total_tokens,
            "metadata": {
                "source_url": source_url,
                "title": title,
                "category": category,
                "chunk_index": 0,
                "total_chunks": 1,
                "scraped_at": scraped_at
            }
        }]

    # Split into overlapping windows
    chunks = []
    start = 0
    chunk_index = 0

    while start < total_tokens:
        # Calculate end position for this chunk
        end = min(start + CHUNK_SIZE, total_tokens)

        # Decode this slice of tokens back to text
        chunk_tokens = tokens[start:end]
        chunk_text = encoder.decode(chunk_tokens)

        chunks.append({
            "chunk_id": f"{_url_to_id(source_url)}_chunk_{chunk_index}",
            "content": chunk_text,
            "token_count": len(chunk_tokens),
            "metadata": {
                "source_url": source_url,
                "title": title,
                "category": category,
                "chunk_index": chunk_index,
                "total_chunks": 0,  # Updated after all chunks created
                "scraped_at": scraped_at
            }
        })

        chunk_index += 1

        # If we've reached the end, stop
        if end == total_tokens:
            break

        # Move forward by chunk_size minus overlap
        # This creates the overlapping window
        start += (CHUNK_SIZE - CHUNK_OVERLAP)

    # Now we know total chunks — update all metadata
    total_chunks = len(chunks)
    for chunk in chunks:
        chunk["metadata"]["total_chunks"] = total_chunks

    return chunks

def _url_to_id(url):
    """
    Convert a URL to a clean identifier string.
    e.g. .../fortnite/functions-in-verse -> functions-in-verse
    """
    # Take the last part of the URL path
    path = url.rstrip("/").split("/")[-1]
    # Remove special characters
    path = re.sub(r'[^a-zA-Z0-9_-]', '_', path)
    return path

def send_chunks_to_sqs(chunks):
    """
    Send chunks to SQS queue in batches of 10.
    SQS supports a maximum of 10 messages per batch request.
    Returns counts of successful and failed sends.
    """
    success_count = 0
    failed_count = 0

    # Process in batches of 10
    batch_size = 10
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]

        # Build SQS batch entries
        entries = []
        for j, chunk in enumerate(batch):
            entries.append({
                "Id": str(j),  # Unique ID within this batch
                "MessageBody": json.dumps(chunk),
                "MessageAttributes": {
                    "category": {
                        "StringValue": chunk["metadata"]["category"],
                        "DataType": "String"
                    },
                    "chunk_id": {
                        "StringValue": chunk["chunk_id"],
                        "DataType": "String"
                    }
                }
            })

        try:
            response = sqs_client.send_message_batch(
                QueueUrl=SQS_QUEUE_URL,
                Entries=entries
            )

            # Count successes and failures from response
            success_count += len(response.get("Successful", []))
            failed_in_batch = response.get("Failed", [])
            failed_count += len(failed_in_batch)

            if failed_in_batch:
                print(f"WARNING: {len(failed_in_batch)} messages failed in batch")
                for failure in failed_in_batch:
                    print(f"  Failed: {failure.get('Id')} -- {failure.get('Message')}")

        except Exception as e:
            print(f"ERROR sending batch to SQS: {e}")
            failed_count += len(batch)

    return success_count, failed_count

def lambda_handler(event, context):
    """
    Main Lambda entry point.
    Triggered by S3 upload events when files land in raw/ folder.
    """
    print(f"DocumentProcessor invoked")
    print(f"Event: {json.dumps(event)}")

    processed = 0
    failed = 0
    total_chunks = 0

    # S3 events can contain multiple records
    # (usually just 1 but we handle multiple to be safe)
    for record in event.get("Records", []):

        # ── Extract S3 bucket and key from event ──────────────
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        print(f"\nProcessing: s3://{bucket}/{key}")

        try:
            # ── Download document from S3 ──────────────────────
            print(f"  Downloading from S3...")
            response = s3_client.get_object(Bucket=bucket, Key=key)
            doc = json.loads(response["Body"].read().decode("utf-8"))

            # ── Validate document has required fields ──────────
            required_fields = ["content", "url", "title", "category", "scraped_at"]
            missing = [f for f in required_fields if f not in doc]
            if missing:
                print(f"  ERROR: Missing required fields: {missing}")
                failed += 1
                continue

            # ── Skip documents with very short content ─────────
            if len(doc["content"]) < 100:
                print(f"  SKIPPING: Content too short ({len(doc['content'])} chars)")
                failed += 1
                continue

            # ── Chunk the document ─────────────────────────────
            print(f"  Chunking document...")
            print(f"  Content length: {len(doc['content'])} chars")

            chunks = chunk_document(
                text=doc["content"],
                source_url=doc["url"],
                title=doc["title"],
                category=doc["category"],
                scraped_at=doc["scraped_at"]
            )

            print(f"  Produced {len(chunks)} chunks")
            for i, chunk in enumerate(chunks):
                print(f"    Chunk {i}: {chunk['token_count']} tokens")

            # ── Send chunks to SQS ─────────────────────────────
            print(f"  Sending to SQS...")
            success, failed_sqs = send_chunks_to_sqs(chunks)
            print(f"  SQS result: {success} sent, {failed_sqs} failed")

            total_chunks += success
            processed += 1

        except Exception as e:
            print(f"  ERROR processing {key}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    # ── Summary ────────────────────────────────────────────────
    summary = {
        "processed_documents": processed,
        "failed_documents": failed,
        "total_chunks_queued": total_chunks,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    print(f"\nSummary: {json.dumps(summary)}")

    return {
        "statusCode": 200,
        "body": json.dumps(summary)
    }



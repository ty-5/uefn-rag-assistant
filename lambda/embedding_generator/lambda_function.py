import json
import boto3
import psycopg2
import os

bedrock = boto3.client("bedrock-runtime", region_name=os.environ.get("BEDROCK_REGION", "us-east-1"))
secretsmanager = boto3.client("secretsmanager", region_name="us-east-1")

_db_credentials = None

def get_db_credentials():
    global _db_credentials
    if _db_credentials is not None:
        return _db_credentials
    secret_name = os.environ.get("SECRET_NAME", "uefn-rag-db-credentials")
    response = secretsmanager.get_secret_value(SecretId=secret_name)
    _db_credentials = json.loads(response["SecretString"])
    return _db_credentials

def get_db_connection():
    creds = get_db_credentials()
    return psycopg2.connect(
        host=creds["host"],
        port=creds["port"],
        dbname=creds["dbname"],
        user=creds["username"],
        password=creds["password"],
        connect_timeout=10,
        sslmode='require'
    )

def generate_embedding(text):
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=json.dumps({"inputText": text})
    )
    body = json.loads(response["body"].read())
    return body["embedding"]

def upsert_document(conn, chunk):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO documents (chunk_id, content, embedding, metadata, source_type, source_url)
            VALUES (%s, %s, %s::vector, %s, %s, %s)
            ON CONFLICT (chunk_id) DO UPDATE SET
                content = EXCLUDED.content,
                embedding = EXCLUDED.embedding,
                metadata = EXCLUDED.metadata,
                updated_at = NOW()
        """, (
            chunk["chunk_id"],
            chunk["content"],
            json.dumps(chunk["embedding"]),
            json.dumps(chunk.get("metadata", {})),
            chunk.get("source_type") or chunk.get("metadata", {}).get("category", "unknown"),
            chunk.get("source_url", "")
        ))
    conn.commit()

def lambda_handler(event, context):
    records = event.get("Records", [])
    print(f"Processing batch of {len(records)} messages")

    processed = 0
    failed = 0
    conn = None

    try:
        conn = get_db_connection()

        for record in records:
            try:
                body = json.loads(record["body"])
                chunk_id = body.get("chunk_id", "unknown")
                print(f"Processing chunk: {chunk_id}")

                embedding = generate_embedding(body["content"])
                body["embedding"] = embedding

                upsert_document(conn, body)
                processed += 1
                print(f"Successfully embedded chunk: {chunk_id}")

            except Exception as e:
                print(f"Failed to process chunk: {str(e)}")
                failed += 1

    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

    print(f"Batch complete - processed: {processed}, failed: {failed}")
    return {"processed": processed, "failed": failed}
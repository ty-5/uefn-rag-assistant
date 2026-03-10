import json
import time
import boto3
import psycopg2
from botocore.exceptions import ClientError

# ── Module-level initialization (runs once on cold start, reused on warm) ──
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
secrets = boto3.client("secretsmanager", region_name="us-east-1")

_db_credentials = None

def get_db_credentials():
    global _db_credentials
    if _db_credentials is None:
        secret = secrets.get_secret_value(SecretId="uefn-rag-db-credentials")
        _db_credentials = json.loads(secret["SecretString"])
    return _db_credentials

def get_embedding(text):
    """Convert text to a 1536-dimension vector using Bedrock Titan."""
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=json.dumps({"inputText": text})
    )
    return json.loads(response["body"].read())["embedding"]

def search_documents(cursor, query_embedding, match_count=5, match_threshold=0.5):  # changed from 0.7 -> 0.5 for large semantic gap between FAQs and actual documentation language
    """Find the most relevant chunks using cosine similarity."""
    cursor.execute(
        "SELECT * FROM search_documents(%s::vector, %s, %s)",
        (query_embedding, match_threshold, match_count)
    )
    return cursor.fetchall()

def build_context(chunks):
    """Assemble retrieved chunks into a context string for Claude."""
    context_parts = []
    for i, chunk in enumerate(chunks):
        metadata = chunk[3] if chunk[3] else {}
        source_url = chunk[5] or metadata.get('source_url', 'Unknown source')
        context_parts.append(f"[Source {i+1}: {source_url}]\n{chunk[2]}")
    return "\n\n---\n\n".join(context_parts)

def query_claude(context, question):
    """Send context + question to Claude and get an answer."""
    prompt = f"""You are an expert UEFN (Unreal Editor for Fortnite) development assistant. 
Answer the user's question using ONLY the documentation context provided below.
If the answer is not in the context, say so clearly rather than guessing.
Always cite which sources you used in your answer.
Include code examples where relevant.

DOCUMENTATION CONTEXT:
{context}

USER QUESTION:
{question}"""

    response = bedrock.invoke_model(
        modelId="us.anthropic.claude-sonnet-4-20250514-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.3,
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    return json.loads(response["body"].read())["content"][0]["text"]

def format_sources(chunks):
    """Build the sources list for the response."""
    sources = []
    for i, chunk in enumerate(chunks):
        metadata = chunk[3] if chunk[3] else {}
        source_url = chunk[5] or metadata.get('source_url', 'Unknown')
        sources.append({
            "index": i + 1,
            "source_url": source_url,
            "source_type": chunk[4] if chunk[4] else "Unknown",
            "similarity_score": round(float(chunk[6]), 3) if chunk[6] else 0
        })
    return sources

def lambda_handler(event, context):
    start_time = time.time()

    # ── Parse request ──────────────────────────────────────────────────────
    try:
        body = json.loads(event.get("body", "{}"))
        question = body.get("question", "").strip()
        max_results = int(body.get("max_results", 5))
    except Exception:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Invalid request body"})
        }

    if not question or len(question) < 3:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Question must be at least 3 characters"})
        }

    conn = None
    try:
        # ── Generate query embedding ───────────────────────────────────────
        query_embedding = get_embedding(question)

        # ── Search vector database ─────────────────────────────────────────
        creds = get_db_credentials()
        conn = psycopg2.connect(
            host=creds["host"],
            port=creds["port"],
            database=creds["dbname"],
            user=creds["username"],
            password=creds["password"],
            sslmode="require",
            connect_timeout=10
        )
        cursor = conn.cursor()
        chunks = search_documents(cursor, query_embedding, max_results)

        if not chunks:
            return {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({
                    "answer": "I couldn't find relevant UEFN documentation for your question. Try rephrasing or asking about a specific Verse API, device, or workflow.",
                    "sources": [],
                    "query_time_ms": int((time.time() - start_time) * 1000)
                })
            }

        # ── Build context and query Claude ────────────────────────────────
        context = build_context(chunks)
        answer = query_claude(context, question)
        sources = format_sources(chunks)
        query_time_ms = int((time.time() - start_time) * 1000)

        print(f"Query: '{question}' | Chunks: {len(chunks)} | Time: {query_time_ms}ms")

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "answer": answer,
                "sources": sources,
                "query_time_ms": query_time_ms
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Internal server error", "detail": str(e)})
        }

    finally:
        if conn:
            conn.close()
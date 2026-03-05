# upload_to_s3.py
import boto3
import json
import os

BUCKET_NAME = "uefn-rag-docs"
S3_PREFIX = "raw/"
SCRAPED_DIR = "docs/scraped"

s3 = boto3.client("s3", region_name="us-east-1")

files = [
    f for f in os.listdir(SCRAPED_DIR)
    if f.endswith(".json") and not f.startswith("_")
]

print(f"Uploading {len(files)} documents to s3://{BUCKET_NAME}/{S3_PREFIX}")
print()

success = 0
failed = 0

for filename in files:
    filepath = os.path.join(SCRAPED_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        doc = json.load(f)

    s3_key = f"{S3_PREFIX}{doc['category']}/{filename}"

    try:
        s3.upload_file(
            filepath,
            BUCKET_NAME,
            s3_key,
            ExtraArgs={
                "ContentType": "application/json",
                "Metadata": {
                    "category": doc["category"],
                    "scraped_at": doc["scraped_at"],
                    "content_length": str(doc["content_length"])
                }
            }
        )
        print(f"  Uploaded: {s3_key}")
        success += 1

    except Exception as e:
        print(f"  FAILED: {filename} -- {e}")
        failed += 1

print(f"\nUpload complete!")
print(f"  Successful: {success}")
print(f"  Failed:     {failed}")
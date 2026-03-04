import boto3

# Test S3 connection
s3 = boto3.client('s3', region_name='us-east-1')
response = s3.list_buckets()

print('Connected to AWS successfully!')
print('Buckets found:')
for bucket in response['Buckets']:
    print(f"  - {bucket['Name']}")

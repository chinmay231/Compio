import os
from pathlib import Path
from dotenv import load_dotenv
import boto3

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(local_path: str, s3_key: str) -> str:
    file_path = Path(local_path)
    if not file_path.exists():
        raise FileNotFoundError(f"❌ Local file does not exist: {local_path}")

    try:
        s3.upload_file(str(file_path), S3_BUCKET, s3_key)
        s3_uri = f"s3://{S3_BUCKET}/{s3_key}"
        print(f"✅ Uploaded to S3: {s3_uri}")
        return s3_uri
    except Exception as e:
        raise RuntimeError(f"❌ Upload failed for {local_path} to {s3_key}: {e}")

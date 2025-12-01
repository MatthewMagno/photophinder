import io
import uuid
from typing import BinaryIO

import boto3
from botocore.client import Config

from .config import settings


session = boto3.session.Session()
s3_client = session.client(
    "s3",
    endpoint_url=settings.storage_endpoint,
    aws_access_key_id=settings.storage_access_key,
    aws_secret_access_key=settings.storage_secret_key,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
    use_ssl=settings.storage_use_ssl,
)


def upload_file(file_bytes: bytes, key: str) -> None:
    s3_client.put_object(Bucket=settings.storage_bucket, Key=key, Body=file_bytes)


def generate_url(key: str) -> str:
    if settings.storage_use_ssl:
        scheme = "https"
    else:
        scheme = "http"
    endpoint = settings.storage_endpoint.rstrip("/").replace("http://", "").replace("https://", "")
    return f"{scheme}://{endpoint}/{settings.storage_bucket}/{key}"


def build_key(prefix: str, suffix: str) -> str:
    return f"{prefix}/{uuid.uuid4()}{suffix}"

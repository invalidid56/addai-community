from fastapi import UploadFile
from config import S3_BUCKET, SITE_ENV
import boto3
from botocore.exceptions import ClientError


s3_client = boto3.client("s3")


def upload_images_to_s3(
    prefix: str,
    name_key: str,
    images: list[UploadFile] = None,
) -> list[str]:
    image_urls = []
    if not images:
        return []

    if SITE_ENV != "local":
        for idx, image in enumerate(images):
            try:
                key = f"{prefix}/{name_key}/{idx}.jpeg"
                s3_client.upload_fileobj(image.file, S3_BUCKET, key, ExtraArgs={"ACL": "public-read"})
                image_urls.append(f"https://{S3_BUCKET}.s3.ap-northeast-2.amazonaws.com/{key}")
            except ClientError as e:
                print(e)
    return image_urls


def upload_one_image_to_s3(prefix: str, name_key: str, image: UploadFile | None = None) -> str:
    if not image:
        return None
    if SITE_ENV != "local":
        try:
            key = f"{prefix}/{name_key}.jpeg"
            s3_client.upload_fileobj(image.file, S3_BUCKET, key, ExtraArgs={"ACL": "public-read"})
            return f"https://{S3_BUCKET}.s3.ap-northeast-2.amazonaws.com/{key}"
        except ClientError as e:
            print(e)


from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from datetime import timedelta
import io


class MinIOClient:
    """MinIO S3-compatible storage client"""
    
    def __init__(self):
        self.client = None
        self.bucket_name = settings.MINIO_BUCKET
    
    def initialize(self):
        """Initialize MinIO client"""
        if self.client is None:
            self.client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            
            # Create bucket if not exists
            try:
                if not self.client.bucket_exists(self.bucket_name):
                    self.client.make_bucket(self.bucket_name)
            except S3Error as e:
                print(f"Error creating bucket: {e}")
    
    def upload_file(self, file_path: str, object_name: str) -> str:
        """Upload file to MinIO"""
        self.initialize()
        
        try:
            self.client.fput_object(
                self.bucket_name,
                object_name,
                file_path
            )
            return object_name
        except S3Error as e:
            raise Exception(f"Failed to upload file: {e}")
    
    def upload_bytes(self, data: bytes, object_name: str, content_type: str = "application/octet-stream") -> str:
        """Upload bytes to MinIO"""
        self.initialize()
        
        try:
            data_stream = io.BytesIO(data)
            self.client.put_object(
                self.bucket_name,
                object_name,
                data_stream,
                length=len(data),
                content_type=content_type
            )
            return object_name
        except S3Error as e:
            raise Exception(f"Failed to upload bytes: {e}")
    
    def get_presigned_url(self, object_name: str, expires: int = 3600, filename: str = None) -> str:
        """Get presigned download URL with optional filename for Content-Disposition"""
        self.initialize()
        
        try:
            # If filename is provided, set response headers for proper download
            response_headers = None
            if filename:
                from urllib.parse import quote
                response_headers = {
                    "response-content-disposition": f'attachment; filename="{quote(filename)}"',
                    "response-content-type": "application/zip"
                }
            
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=timedelta(seconds=expires),
                response_headers=response_headers
            )
            return url
        except S3Error as e:
            raise Exception(f"Failed to generate presigned URL: {e}")
    
    def delete_file(self, object_name: str):
        """Delete file from MinIO"""
        self.initialize()
        
        try:
            self.client.remove_object(self.bucket_name, object_name)
        except S3Error as e:
            raise Exception(f"Failed to delete file: {e}")


# Singleton instance
minio_client = MinIOClient()

from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from datetime import timedelta
import io
import os
from pathlib import Path


class MinIOClient:
    """MinIO S3-compatible storage client with local fallback"""
    
    def __init__(self):
        self.client = None
        self.bucket_name = settings.MINIO_BUCKET
        self.enabled = getattr(settings, 'MINIO_ENABLED', True)
        self.local_storage_path = Path("./storage/projects")
    
    def initialize(self):
        """Initialize MinIO client if enabled"""
        if not self.enabled:
            # Ensure local storage directory exists
            self.local_storage_path.mkdir(parents=True, exist_ok=True)
            return
            
        if self.client is None:
            try:
                self.client = Minio(
                    settings.MINIO_ENDPOINT,
                    access_key=settings.MINIO_ACCESS_KEY,
                    secret_key=settings.MINIO_SECRET_KEY,
                    secure=settings.MINIO_SECURE
                )
                
                # Create bucket if not exists
                if not self.client.bucket_exists(self.bucket_name):
                    self.client.make_bucket(self.bucket_name)
            except Exception as e:
                print(f"Warning: MinIO connection failed: {e}. Falling back to local storage.")
                self.enabled = False
                self.local_storage_path.mkdir(parents=True, exist_ok=True)
    
    def _get_local_path(self, object_name: str) -> Path:
        """Get local file path for an object"""
        return self.local_storage_path / object_name.replace("/", os.sep)
    
    def upload_file(self, file_path: str, object_name: str) -> str:
        """Upload file to MinIO or local storage"""
        self.initialize()
        
        if not self.enabled or not self.client:
            # Use local filesystem storage
            local_path = self._get_local_path(object_name)
            local_path.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(file_path, local_path)
            print(f"File saved to local storage: {local_path}")
            return object_name
        
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
        """Upload bytes to MinIO or local storage"""
        self.initialize()
        
        if not self.enabled or not self.client:
            # Use local filesystem storage
            local_path = self._get_local_path(object_name)
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(data)
            print(f"Bytes saved to local storage: {local_path}")
            return object_name
        
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
    
    def get_bytes(self, object_name: str) -> bytes:
        """Get bytes from MinIO or local storage"""
        self.initialize()
        
        if not self.enabled or not self.client:
            # Read from local filesystem
            local_path = self._get_local_path(object_name)
            if local_path.exists():
                return local_path.read_bytes()
            raise Exception(f"File not found: {object_name}")
        
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            return response.read()
        except S3Error as e:
            raise Exception(f"Failed to get file: {e}")
    
    def get_presigned_url(self, object_name: str, expires: int = 3600, filename: str = None) -> str:
        """Get presigned download URL or local reference"""
        self.initialize()
        
        if not self.enabled or not self.client:
            # Return a marker for local storage - the actual URL is constructed by the API
            return f"local://{object_name}"
        
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
    
    def file_exists(self, object_name: str) -> bool:
        """Check if file exists in storage"""
        self.initialize()
        
        if not self.enabled or not self.client:
            local_path = self._get_local_path(object_name)
            return local_path.exists()
        
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error:
            return False
    
    def delete_file(self, object_name: str):
        """Delete file from MinIO or local storage"""
        self.initialize()
        
        if not self.enabled or not self.client:
            local_path = self._get_local_path(object_name)
            if local_path.exists():
                local_path.unlink()
            return
        
        try:
            self.client.remove_object(self.bucket_name, object_name)
        except S3Error as e:
            raise Exception(f"Failed to delete file: {e}")


# Singleton instance
minio_client = MinIOClient()


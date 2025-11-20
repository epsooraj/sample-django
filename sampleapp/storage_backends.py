"""
Custom storage backends for S3 storage.
"""
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Custom storage backend for static files in S3.
    Static files will be stored in the location specified by AWS_LOCATION setting.
    """
    # Don't set default_acl here - let it be None if bucket doesn't support ACLs
    default_acl = None


class MediaStorage(S3Boto3Storage):
    """
    Custom storage backend for media files in S3.
    Media files will be stored in the 'media' folder in your S3 bucket.
    Configure AWS_MEDIA_LOCATION in settings to change the folder name.
    """
    location = 'media'
    # Don't set default_acl here - let it be None if bucket doesn't support ACLs
    default_acl = None
    file_overwrite = False
    
    def __init__(self, *args, **kwargs):
        # Import settings here to avoid issues during class definition
        from django.conf import settings
        # Override from settings if available
        if hasattr(settings, 'AWS_MEDIA_LOCATION'):
            self.location = settings.AWS_MEDIA_LOCATION
        if hasattr(settings, 'AWS_DEFAULT_ACL'):
            self.default_acl = settings.AWS_DEFAULT_ACL
        super().__init__(*args, **kwargs)


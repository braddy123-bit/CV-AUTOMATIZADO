"""
Backends de almacenamiento para archivos media
"""

from storages.backends.azure_storage import AzureStorage
from django.conf import settings


class AzureMediaStorage(AzureStorage):
    """
    Storage personalizado para Azure Blob Storage
    """
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.AZURE_CONTAINER
    expiration_secs = None
    overwrite_files = True

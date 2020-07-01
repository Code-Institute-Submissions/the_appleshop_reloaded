from django.test import TestCase
from custom_storages import StaticStorage, MediaStorage
from storages.backends.s3boto3 import S3Boto3Storage
from appleshop.settings import STATICFILES_LOCATION, MEDIAFILES_LOCATION

class TestCustomStorages(TestCase):

    def test_check_settings_custom_storages_StaticStorage(self):
        static_storage = StaticStorage(S3Boto3Storage)
        self.assertEqual(static_storage.location, STATICFILES_LOCATION)

    def test_check_settings_custom_storages_MediaStorage(self):
        media_storage = MediaStorage(S3Boto3Storage)
        self.assertEqual(media_storage.location, MEDIAFILES_LOCATION)
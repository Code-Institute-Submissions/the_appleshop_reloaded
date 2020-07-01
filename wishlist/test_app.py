from django.apps import apps
from django.test import TestCase
from .apps import WishlistConfig


class TestWishlistConfig(TestCase):
    def test_app(self):
        self.assertEqual("wishlist", WishlistConfig.name)
        self.assertEqual("wishlist", apps.get_app_config("wishlist").name)

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Wishlist


class TestWishlistModels(TestCase):
    def test_Wishlist_return_name(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        user_wishlist = Wishlist(user=new_user, name='testusers wishlist',
                                 product_list='1,2')
        self.assertEqual(str(user_wishlist), 'testusers wishlist')

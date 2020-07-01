from django.test import TestCase
from django.contrib.auth.models import User
from .models import Cart


class TestCartModel(TestCase):
    def test_cart_model_return_name(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        cart = Cart(user=new_user, name='testusers cart',
                    product_list="{'1': 11, '2': 22}")
        self.assertEqual(str(cart), "testusers cart")
        self.assertEqual(cart.product_list, "{'1': 11, '2': 22}")

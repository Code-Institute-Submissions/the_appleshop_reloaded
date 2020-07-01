from django.test import TestCase
from products.models import Product
from django.views.generic import View, TemplateView, RedirectView
from django.contrib.auth.models import User
from .models import Cart
from .contexts import merge_carts


class TestCartContexts(TestCase):

    def test_empty_cart_contents(self):
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart, {})

    def test_cart_contents_return_values(self):
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden delicious', description='description', price=1)
        self.client.post('/cart/add/1', data={'quantity': 11})
        self.client.post('/cart/add/2', data={'quantity': 22})
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart, {'1': 11, '2': 22})

    def test_merge_carts_methos(self):
        dic1 = {'1': 11, '2': 22, '3': 33}
        dic2 = {'4': 44, '5': 55, '6': 66}
        dic3 = {'1': 5, '2': 22, '3': 33}
        merged_cart = merge_carts(dic1, dic2)
        self.assertEqual(merged_cart[0]['4'], 44)
        merged_cart = merge_carts(dic1, dic3)
        self.assertEqual(merged_cart[0]['1'], 11)

    def test_sync_carts_with_cart_in_db_and_no_local_cart(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart, {})
        user_cart = Cart.objects.create(user=new_user, name='testusers cart',
                                        product_list={'1': 11, '2': 22})
        self.client.login(username='testuser', password='password')
        response = self.client.get('/products/', content_type="html/text",
                                   follow=True)
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart, {'1': 11, '2': 22})

    def test_sync_carts_no_cart_in_db_and_local_cart(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        cart = self.client.session.get('cart', {})
        self.assertEqual(cart, {})
        self.client.login(username='testuser', password='password')
        self.client.post('/cart/add/1', data={'quantity': 11})
        self.client.post('/cart/add/2', data={'quantity': 22})
        user_cart = Cart.objects.get(user=new_user)
        user_cart.product_list = ""
        user_cart.save()
        self.assertEqual(user_cart.product_list, "")
        response = self.client.get('/products/', content_type="html/text",
                                   follow=True)
        user_cart = Cart.objects.get(user=new_user)
        self.assertEqual(user_cart.product_list, "{'1': 11, '2': 22}")

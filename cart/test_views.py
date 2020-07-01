from django.test import TestCase
from django.contrib.auth.models import User
from .models import Cart
from products.models import Product


class TestAddToCartView(TestCase):

    def test_response_view_cart(self):
        response = self.client.get("/cart/", content_type="html/text",
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart.html")

    def test_add_products_not_being_on_cart(self):
        self.client.post('/cart/add/1', data={'quantity': 11})
        self.client.post('/cart/add/2', data={'quantity': 22})
        cart = self.client.session.get('cart')
        self.assertEqual(cart, {'1': 11, '2': 22})

    def test_add_product_already_being_on_cart(self):
        self.client.post('/cart/add/1', data={'quantity': 11})
        self.client.post('/cart/add/1', data={'quantity': 11})
        cart = self.client.session.get('cart')
        self.assertEqual(cart, {'1': 22})

    def test_add_product_to_cart_when_logged_in(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        self.client.post('/cart/add/1', data={'quantity': 11})
        self.client.post('/cart/add/2', data={'quantity': 22})
        cart = self.client.session.get('cart')
        self.assertEqual(cart, {'1': 11, '2': 22})
        user_cart = Cart.objects.get(user=new_user)
        self.assertEqual(user_cart.product_list, "{'1': 11, '2': 22}")


class TestAdjustCartView(TestCase):

    def test_increase_product_quantity_on_cart(self):
        self.client.post('/cart/add/1', data={'quantity': 11})
        self.client.post('/cart/adjust/1', data={'quantity': 5})
        cart = self.client.session.get('cart')
        self.assertEqual(cart, {'1': 5})

    def test_set_product_quantity_on_cart_to_zero(self):
        self.client.post('/cart/add/1', data={'quantity': 11})
        self.client.post('/cart/adjust/1', data={'quantity': 0})
        cart = self.client.session.get('cart')
        self.assertEqual(cart, {})

    def test_increase_product_quantity_on_cart_when_logged_in(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        self.client.post('/cart/add/1', data={'quantity': 11})
        self.client.post('/cart/adjust/1', data={'quantity': 5})
        cart = self.client.session.get('cart')
        self.assertEqual(cart, {'1': 5})
        user_cart = Cart.objects.get(user=new_user)
        self.assertEqual(user_cart.product_list, "{'1': 5}")

    def test_increase_product_quantity_no_cart_in_db(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        self.client.post('/cart/add/1', data={'quantity': 11})
        self.client.post('/cart/adjust/1', data={'quantity': 5})
        cart = self.client.session.get('cart')
        self.assertEqual(cart, {'1': 5})
        user_cart = Cart.objects.get(user=new_user.id).delete()
        self.client.post('/cart/adjust/1', data={'quantity': 10})
        user_cart = Cart.objects.get(user=new_user)
        self.assertEqual(user_cart.product_list, "{'1': 10}")

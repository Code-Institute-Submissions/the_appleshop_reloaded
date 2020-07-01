from django.test import TestCase
from .forms import MakePaymentForm, OrderForm
from django.contrib.auth.models import User
from .models import OrderLineItem, Order
from cart.models import Cart
from django.utils import timezone
from products.models import Product
from django.conf import settings
import stripe
import os


class TestCheckoutView(TestCase):

    def test_order_and_payment_forms_valid_order_form(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden Delicious', description='description testproduct', price=2)
        self.client.post('/cart/add/1', data={'quantity': '11'})
        self.client.post('/cart/add/2', data={'quantity': '22'})
        user_cart = Cart.objects.get(user=new_user.id)
        self.assertEqual(user_cart.product_list, "{'1': 11, '2': 22}")
        cart = self.client.session.get('cart')
        self.assertEqual(cart, {'1': 11, '2': 22})
        stripe_id = 'tok_mastercard'
        self.client.post('/checkout/', {'full_name': 'John Doe',
                                        'phone_number': '123456789', 'country':
                                        'Netherlands', 'postcode': '1234',
                                        'town_or_city': 'Amsterdam',
                                        'street_address1': 'Street',
                                        'street_address2': '22', 'county':
                                        'North', 'date': '2020-06-09',
                                        'credit_card_number':
                                        '5555555555554444', 'cvv': '111',
                                        'expiry_month': '12', 'expiry_year':
                                        '2022', 'stripe_id': stripe_id})
        check_product = Product.objects.get(pk=1)
        self.assertEqual(check_product.ordered_pcs, 11)
        cart = self.client.session.get('cart')
        self.assertEqual(cart, {})
        user_cart = Cart.objects.get(user=new_user.id)
        self.assertEqual(user_cart.product_list, "")

    def test_order_and_payment_forms_invalid_order_form(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden Delicious', description='description testproduct', price=2)
        self.client.post('/cart/add/1', data={'quantity': '11'})
        self.client.post('/cart/add/2', data={'quantity': '22'})
        stripe_id = 'tok_mastercard'
        response = self.client.post('/checkout/',
                                    {'full_name': '', 'phone_number':
                                     '123456789', 'country': '', 'postcode':
                                     '1234', 'town_or_city': '',
                                     'street_address1': 'Street',
                                     'street_address2': '22', 'county':
                                     'North', 'date': '2020-06-09',
                                     'credit_card_number': '5555555555554444',
                                     'cvv': '111', 'expiry_month': '12',
                                     'expiry_year': '2022',
                                     'stripe_id': stripe_id})
        self.assertIn(b'We were unable to take a payment with that card!',
                      response.content)

    def test_checkout_view_with_get_method(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden Delicious', description='description testproduct', price=2)
        self.client.post('/cart/add/1', data={'quantity': '11'})
        self.client.post('/cart/add/2', data={'quantity': '22'})
        response = self.client.get('/checkout/', content_type="html/text",
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter your shipping address', response.content)

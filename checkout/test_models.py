from django.test import TestCase
from django.db import models
from products.models import Product
from .models import Order, OrderLineItem
from django.contrib.auth.models import User


class TestCheckoutModels(TestCase):

    def test_Order_Model(self):
        order = Order.objects.create(full_name='John Doe',
                                     phone_number='123456789',
                                     country='Netherlands',
                                     postcode='1234',
                                     town_or_city='Amsterdam',
                                     street_address1='Street',
                                     street_address2='22',
                                     county='North',
                                     date='2020-06-09')

        self.assertIn('1-2020-06-09-John Doe', str(order))

    def test_order_line_item_Model(self):
        order = Order.objects.create(full_name='John Doe',
                                     phone_number='123456789',
                                     country='Netherlands',
                                     postcode='1234',
                                     town_or_city='Amsterdam',
                                     street_address1='Street',
                                     street_address2='22',
                                     county='North',
                                     date='2020-06-09')
        product = Product.objects.create(name='testproduct', description='description testproduct', price=2)
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        order_line_item = OrderLineItem(user=new_user, order=order,
                                        product=product,
                                        quantity=2)

        self.assertEqual('2 testproduct @ 2', str(order_line_item))

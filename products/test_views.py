from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from products.views import get_user_purchases
from checkout.models import Order, OrderLineItem


class TestProductsViews(TestCase):

    def test_get_all_products(self):
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product2 = Product.objects.create(name='testproduct2', description='description testproduct2', price=2)
        product3 = Product.objects.create(name='testproduct3', description='description testproduct3', price=3)
        product4 = Product.objects.create(name='testproduct4', description='description testproduct4', price=4)
        response = self.client.get("/products/", content_type="html/text", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products.html")
        self.assertIn(b'testproduct1', response.content)
        self.assertIn(b'testproduct2', response.content)
        self.assertIn(b'testproduct3', response.content)
        self.assertIn(b'testproduct4', response.content)

    def test_get_all_products_as_logged_in_user(self):
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product2 = Product.objects.create(name='testproduct2', description='description testproduct2', price=2)
        product3 = Product.objects.create(name='testproduct3', description='description testproduct3', price=3)
        product4 = Product.objects.create(name='testproduct4', description='description testproduct4', price=4)
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        order = Order.objects.create(full_name='John Doe',
                                     phone_number='123456789',
                                     country='Netherlands', postcode='1234',
                                     town_or_city='Amsterdam',
                                     street_address1='Street',
                                             street_address2='22',
                                             county='North',
                                             date='2020-06-09')

        order_line_item1 = OrderLineItem(user=new_user, order=order,
                                         product=product1, quantity=1)

        order_line_item2 = OrderLineItem(user=new_user, order=order,
                                         product=product2, quantity=2)

        order_line_item3 = OrderLineItem(user=new_user, order=order,
                                         product=product3, quantity=3)

        response = self.client.get("/products/", content_type="html/text",
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testproduct1', response.content)
        self.assertIn(b'testproduct2', response.content)
        self.assertIn(b'testproduct3', response.content)
        self.assertIn(b'testproduct4', response.content)

    def test_get_user_purchases(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product2 = Product.objects.create(name='testproduct2', description='description testproduct2', price=2)
        product3 = Product.objects.create(name='testproduct3', description='description testproduct3', price=3)
        product1.save()
        product2.save()
        product3.save()
        order = Order.objects.create(full_name='John Doe',
                                     phone_number='123456789',
                                     country='Netherlands',
                                     postcode='1234',
                                     town_or_city='Amsterdam',
                                     street_address1='Street',
                                             street_address2='22',
                                             county='North',
                                             date='2020-06-09')
        order_line_item1 = OrderLineItem(user=new_user, order=order,
                                         product=product1, quantity=1)
        order_line_item1.save()
        order_line_item2 = OrderLineItem(user=new_user, order=order,
                                         product=product2, quantity=2)
        order_line_item2.save()
        order_line_item3 = OrderLineItem(user=new_user, order=order,
                                         product=product3, quantity=3)
        order_line_item3.save()
        self.assertEqual(get_user_purchases(new_user),
                         ['testproduct1', 'testproduct2', 'testproduct3'])

    def test_product_detail_view(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product1.save()
        order = Order.objects.create(full_name='John Doe',
                                     phone_number='123456789',
                                     country='Netherlands',
                                     postcode='1234',
                                     town_or_city='Amsterdam',
                                     street_address1='Street',
                                     street_address2='22',
                                     county='North',
                                     date='2020-06-09')
        order_line_item1 = OrderLineItem(user=new_user, order=order,
                                         product=product1, quantity=1)
        order_line_item1.save()
        response = self.client.get('/products/1', content_type="html/text",
                                   follow=True)
        check_product = Product.objects.get(pk=1)
        self.assertEqual(check_product.view_count, 1)
        self.assertEqual(get_user_purchases(new_user), ['testproduct1'])

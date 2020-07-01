from django.test import TestCase
from django.shortcuts import get_object_or_404
from .models import Review
from django.contrib.auth.models import User
from products.models import Product
from checkout.models import Order, OrderLineItem


class TestReviewViews(TestCase):

    def test_get_reviews_view(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product1.save()
        new_review = Review(title="review name", product=product1, author=new_user, rating=5, comment="Fantastic!")
        new_review.save()
        response = self.client.get('/reviews/', content_type="html/text",
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews.html")
        self.assertIn(b'Fantastic!', response.content)

    def test_review_detail_view(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product1.save()
        new_review = Review(title="review name", product=product1, author=new_user, rating=5, comment="Fantastic!")
        new_review.save()
        response = self.client.get('/reviews/1', content_type="html/text", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviewdetail.html")
        self.assertIn(b'Fantastic!', response.content)
        check_review = Review.objects.get(pk=1)
        self.assertEqual(check_review.view_count, 1)

    def test_create_review_view(self):
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
        order_line_item = OrderLineItem(user=new_user, order=order,
                                        product=product1, quantity=2)
        order_line_item.save()
        response = self.client.get('/reviews/new/1', content_type="html/text",
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "editform.html")
        self.assertIn(b'required-field', response.content)

    def test_create_review_notpurchased_product_view(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product1.save()
        product2 = Product.objects.create(name='testproduct2', description='description testproduct2', price=1)
        product2.save()
        order = Order.objects.create(full_name='John Doe',
                                     phone_number='123456789',
                                     country='Netherlands',
                                     postcode='1234',
                                     town_or_city='Amsterdam',
                                     street_address1='Street',
                                     street_address2='22',
                                     county='North',
                                     date='2020-06-09')
        order_line_item = OrderLineItem(user=new_user, order=order,
                                        product=product2, quantity=2)
        order_line_item.save()
        response = self.client.get('/reviews/new/1', content_type="html/text",
                                   follow=True)
        self.assertTemplateUsed("reviews.html")

    def test_create_review_with_post_valid_form_view(self):
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
        order_line_item = OrderLineItem(user=new_user, order=order,
                                        product=product1, quantity=2)
        order_line_item.save()
        self.client.post('/reviews/new/1',
                         data={'title': 'review name', 'product': product1,
                               'author': new_user, 'rating': 5, 'comment':
                               'Fantastic!'})

        self.assertTemplateUsed("reviewdetail.html")

    def test_edit_review_get_view(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product1.save()
        new_review = Review(title="review name", product=product1, author=new_user, rating=5, comment="Fantastic!")
        new_review.save()
        response = self.client.get('/reviews/1/edit/',
                                   content_type="html/text", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "editform.html")
        self.assertIn(b'Fantastic!', response.content)

    def test_edit_review_get_notloggedin_view(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product1.save()
        new_review = Review(title="review name", product=product1,
                            author=new_user, rating=5, comment="Fantastic!")
        new_review.save()
        response = self.client.get('/reviews/1/edit/',
                                   content_type="html/text", follow=True)
        self.assertTemplateUsed("reviews.html")

    def test_edit_review_post_view(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product1.save()
        new_review = Review(title="review name", product=product1, author=new_user, rating=5, comment="Fantastic!")
        new_review.save()
        self.client.post('/reviews/1/edit/',
                         data={'title': 'title changed', 'rating': 3,
                               'comment': 'tasty'})
        self.assertTemplateUsed("reviewdetail.html")

    def test_delete_review(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product1.save()
        new_review = Review.objects.create(title="review name", product=product1, author=new_user, rating=5, comment="Fantastic!")
        new_review.save()
        check_review = Review.objects.get(pk=1)
        self.assertEqual(str(check_review), "review name")
        self.client.get('/reviews/1/delete/')
        reviews = Review.objects.all()
        self.assertEqual(list(reviews), [])

    def test_delete_review_notloggedin(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        product1 = Product.objects.create(name='testproduct1', description='description testproduct1', price=1)
        product1.save()
        new_review = Review.objects.create(title="review name", product=product1, author=new_user, rating=5, comment="Fantastic!")
        new_review.save()
        self.client.post('/reviews/1/delete/')
        self.assertTemplateUsed("reviews.html")

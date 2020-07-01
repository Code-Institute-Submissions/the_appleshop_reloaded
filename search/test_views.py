from django.test import TestCase
from products.models import Product
from django.contrib.auth.models import User
from reviews.models import Review


class TestSearchViews(TestCase):
    def test_product_search(self):
        product = Product.objects.create(name='testproduct', description='description testproduct', price=2)
        page = self.client.post("/search/product_search/",
                                data={'q': product.name}, follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "products.html")
        self.assertIn(b'testproduct', page.content)

    def test_review_search(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product = Product.objects.create(name='testproduct', description='description testproduct', price=2)
        product.save()
        new_review = Review.objects.create(title="review name", product=product, author=new_user, rating=5, comment="Fantastic!")
        new_review.save()
        page = self.client.post("/search/review_search/", data={'q': product.name}, follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "reviews.html")
        self.assertIn(b'review name', page.content)

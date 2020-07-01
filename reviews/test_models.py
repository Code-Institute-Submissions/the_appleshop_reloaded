from django.test import TestCase
from django.contrib.auth.models import User
from .models import Review
from products.models import Product


class TestReviewModel(TestCase):

    def test_create_review_model_and_check_return_value(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        new_review = Review(title="review name", author=new_user, rating=5,
                            comment="Fantastic!")
        self.assertEqual(new_review.title, "review name")
        self.assertEqual(str(new_review.author), "testuser")
        self.assertEqual(new_review.rating, 5)
        self.assertEqual(new_review.comment, "Fantastic!")
        self.assertEqual(str(new_review), "review name")

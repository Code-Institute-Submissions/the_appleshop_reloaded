from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from .models import Wishlist


class TestWishlistViews(TestCase):
    def test_response_wishlist_view(self):
        response = self.client.get("/wishlist/", content_type="html/text",
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wishlist.html")

    def test_remove_from_wishlist_when_logged_out(self):
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden delicious', description='description', price=1)
        self.client.post('/wishlist/add/1')
        self.client.post('/wishlist/add/2')
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [1, 2])
        self.client.post('/wishlist/remove/1')
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [2])

    def test_remove_from_wishlist_when_logged_in(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden delicious', description='description', price=1)
        self.client.post('/wishlist/add/1')
        self.client.post('/wishlist/add/2')
        self.client.post('/wishlist/remove/1')
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [2])

    def test_remove_from_wishlist_when_logged_in_no_wishlist_in_db(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden delicious', description='description', price=1)
        self.client.post('/wishlist/add/1')
        self.client.post('/wishlist/add/2')
        user_wishlist = Wishlist.objects.get(user=new_user.id).delete()
        self.client.post('/wishlist/remove/1')
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [2])
        user_wishlist = Wishlist.objects.get(user=new_user.id)
        user_wishlist.product_list = '2'

    def test_remove_from_wishlist_with_get_method_logged_in(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        user_wishlist = Wishlist(user=new_user, name='name', product_list="")
        user_wishlist.save()
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden delicious', description='description', price=1)
        self.client.post('/wishlist/add/1')
        self.client.post('/wishlist/add/2')
        response = self.client.get("/wishlist/remove/1",
                                   content_type="html/text", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wishlist.html")

from django.test import TestCase
from products.models import Product
from django.views.generic import View, TemplateView, RedirectView
from django.contrib.auth.models import User
from .models import Wishlist
from .contexts import make_wishlist_string, make_wishlist_list, merge_wishlists, sync_wishlists, wishlist_contents


class TestWishlistContexts(TestCase):

    def test_empty_wishlist_contents(self):
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [])

    def test_wishlist_contents_return_values(self):
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden delicious', description='description', price=1)
        self.client.post('/wishlist/add/1')
        self.client.post('/wishlist/add/2')
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [1, 2])
        self.assertEqual(len(wishlist), 2)
        response = self.client.get('/products/', content_type="html/text",
                                   follow=True)
        self.assertIn(b'Boskop', response.content)
        self.assertIn(b'Golden delicious', response.content)


class TestWishlistMethods(TestCase):

    def test_make_wishlist_string(self):
        wishlist = [1, 2]
        self.assertEqual(make_wishlist_string(wishlist), '1,2')

    def test_make_wishlist_list_with_empty_product_list(self):
        productlist = ""
        self.assertEqual(make_wishlist_list(productlist), [])

    def test_make_wishlist_list_with_with_product_list(self):
        productlist = '1,2'
        self.assertEqual(make_wishlist_list(productlist), [1, 2])

    def test_merge_wishlists_both_lists_different_values(self):
        tmp_wishlist_from_db = [1, 3]
        wishlist = [4, 5]
        self.assertEqual(merge_wishlists(tmp_wishlist_from_db, wishlist),
                         [4, 5, 1, 3])

    def test_merge_wishlists_one_list_contains_other_list_value(self):
        tmp_wishlist_from_db = [1, 2]
        wishlist = [2]
        self.assertEqual(merge_wishlists(tmp_wishlist_from_db, wishlist),
                         [2, 1])

    def test_merge_wishlists_tmp_list_empty(self):
        tmp_wishlist_from_db = []
        wishlist = [2]
        self.assertEqual(merge_wishlists(tmp_wishlist_from_db, wishlist), [2])

    def test_merge_wishlists_wishlist_empty(self):
        tmp_wishlist_from_db = [1, 2]
        wishlist = []
        self.assertEqual(merge_wishlists(tmp_wishlist_from_db, wishlist),
                         [1, 2])

    def test_sync_wishlists_with_wishlist_in_db_and_locallist(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden delicious', description='description', price=1)
        product4 = Product.objects.create(name='Elstar', description='description testproduct', price=2)
        product5 = Product.objects.create(name='Junami', description='description', price=1)
        self.client.post('/wishlist/add/1')
        self.client.post('/wishlist/add/2')
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [1, 2])
        user_wishlist = Wishlist.objects.get(user=new_user.id)
        self.assertEqual(user_wishlist.product_list, '1,2')
        user_wishlist = Wishlist.objects.get(user=new_user.id)
        user_wishlist.product_list = '4,5'
        user_wishlist.save()
        user_wishlist = Wishlist.objects.get(user=new_user.id)
        self.assertEqual(user_wishlist.product_list, '4,5')
        response = self.client.get('/products/', content_type="html/text",
                                   follow=True)
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [1, 2, 4, 5])
        user_wishlist = Wishlist.objects.get(user=new_user.id)
        self.assertEqual(user_wishlist.product_list, '1,2,4,5')

    def test_sync_wishlist_with_db_wishlist_and_no_locallist(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [])
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden delicious', description='description', price=1)
        product4 = Product.objects.create(name='Elstar', description='description testproduct', price=2)
        product5 = Product.objects.create(name='Junami', description='description', price=1)
        response = self.client.get('/products/', content_type="html/text",
                                   follow=True)
        user_wishlist = Wishlist.objects.get(user=new_user.id)
        user_wishlist.product_list = '4, 5'
        user_wishlist.save()
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [])
        response = self.client.get('/products/', content_type="html/text",
                                   follow=True)
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [4, 5])

    def test_sync_wishlists_with_empty_db_wishlist_and_locallist(self):
        product1 = Product.objects.create(name='Boskop', description='description testproduct', price=2)
        product2 = Product.objects.create(name='Golden delicious', description='description', price=1)
        wishlist = self.client.session.get('wishlist', [])
        self.assertEqual(wishlist, [])
        self.client.post('/wishlist/add/1')
        self.client.post('/wishlist/add/2')
        wishlist = self.client.session.get('wishlist')
        self.assertEqual(wishlist, [1, 2])
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        response = self.client.get('/products/', content_type="html/text",
                                   follow=True)
        user_wishlist = Wishlist.objects.get(user=new_user.id)
        self.assertEqual(user_wishlist.product_list, '1,2')

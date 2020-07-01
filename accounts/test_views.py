from django.test import TestCase
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegistrationForm, UserAddressForm
from .models import UserAddress


class TestAccountsRegistrationView(TestCase):

    def test_registration_page_response(self):
        page = self.client.get("/accounts/register/", content_type="html/text",
                               follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "registration.html")

    def test_diverting_to_index_when_trying_to_register_and_logged_in(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        page = self.client.get("/accounts/register/", content_type="html/text",
                               follow=True)
        self.assertTemplateUsed(page, "bestsellers.html")

    def test_unique_email_address_in_registration_form(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        response = self.client.post('/accounts/register/',
                                    data={'username': 'testuser', 'email':
                                          'testuser@domain.com', 'password1':
                                          'password', 'password2': 'password'})
        self.assertIn(b'Email address must be unique', response.content)


class TestAccountsLoginView(TestCase):

    def test_login_page_response(self):
        page = self.client.get("/accounts/login/", content_type="html/text",
                               follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "login.html")

    def test_login_with_correct_password(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        response = self.client.post('/accounts/login/',
                                    data={'username': 'testuser', 'password':
                                          'password'}, follow=True)
        self.assertTemplateUsed(response, "profile.html")
        self.assertIn(b'You have successfully logged in!', response.content)

    def test_login_with_incorrect_password(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        response = self.client.post('/accounts/login/',
                                    data={'username': 'testuser', 'password':
                                          'none'}, follow=True)
        self.assertTemplateUsed(response, "login.html")
        self.assertIn(b'Your username and password is incorrect',
                      response.content)

    def test_create_login_form_from_user_entered_formdata(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        response = self.client.post('/accounts/login/',
                                    data={'username': 'testuser', 'password':
                                          'password'}, follow=True)
        self.assertIn(b'You have successfully logged in!', response.content)


class TestAccountsLogoutView(TestCase):

    def test_logout_state(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        page = self.client.get("/accounts/logout/", content_type="html/text",
                               follow=True)
        self.assertIn(b"You have successfully been logged out!", page.content)


class TestAccountsProfileView(TestCase):
    def test_call_profilepage_divert_to_loginpage_when_logged_out(self):
        page = self.client.get("/accounts/profile/", content_type="html/text",
                               follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "login.html")

    def test_divert_to_profilepage_when_logged_in(self):
        self.client.post('/accounts/register/',
                         data={'username': 'testuser', 'email':
                               'testuser@domain.com', 'password1': 'password',
                               'password2': 'password'})
        self.client.post('/accounts/login/', data={'username': 'testuser',
                                                   'password': 'password'})
        page = self.client.get("/accounts/login/", content_type="html/text",
                               follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, "profile.html")
        self.assertIn(b"Update Address!", page.content)

    def test_post_an_address_in_profile_view(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        self.client.login(username='testuser', password='password')
        user_address = UserAddress.objects.create(user=new_user)
        page = self.client.get("/accounts/profile/", content_type="html/text",
                               follow=True)
        self.client.post('/accounts/profile/',
                         {'full_name': 'John Doe', 'phone_number': '123456789',
                          'country': 'Netherlands', 'postcode': '1234',
                          'town_or_city': 'Amsterdam', 'street_address1':
                          'Street', 'street_address2': '22', 'county':
                          'North'})
        new_address = UserAddress.objects.get(user=new_user.id)
        self.assertEqual(new_address.full_name, "John Doe")

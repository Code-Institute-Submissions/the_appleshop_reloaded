from django.test import TestCase
from django.contrib.auth.models import User


class TestAccountsForms(TestCase):

    def test_unique_email_address_in_registration_form(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        response = self.client.post('/accounts/register/',
                                    data={'username': 'testuser', 'email':
                                          'testuser@domain.com', 'password1':
                                          'password', 'password2': 'password'})
        self.assertIn(b'Email address must be unique', response.content)

    def test_missing_passwords_registration_form(self):
        response = self.client.post('/accounts/register/',
                                    data={'username': 'testuser', 'email':
                                          'testuser@domain.com', 'password1':
                                          'password', 'password2': ''})
        self.assertIn(b'This field is required.', response.content)

    def test_not_matching_passwords_registration_form(self):
        response = self.client.post('/accounts/register/',
                                    data={'username': 'testuser', 'email':
                                          'testuser@domain.com', 'password1':
                                          'password', 'password2': 'none'})
        self.assertIn(b'Passwords must match', response.content)

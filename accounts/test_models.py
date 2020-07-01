from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from .models import UserAddress


class TestUserAddressModel(TestCase):

    def test_UserAddress_Model(self):
        new_user = User.objects.create_user('testuser', 'testuser@domain.com',
                                            'password')
        new_address = UserAddress.objects.create(user=new_user,
                                                 full_name='John Doe',
                                                 phone_number='123456789',
                                                 country='Netherlands',
                                                 postcode='1234',
                                                 town_or_city='Amsterdam',
                                                 street_address1='Street',
                                                 street_address2='22',
                                                 county='North')
        self.assertIn('John Doe', str(new_address))

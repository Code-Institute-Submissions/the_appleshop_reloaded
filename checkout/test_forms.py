from django.test import TestCase
from .forms import OrderForm


class TestCheckoutOrderForm(TestCase):

    def test_can_create_an_orderform_with_name(self):
        form = OrderForm({'full_name': 'John Doe', 'phone_number': '123456789',
                          'country': 'Netherlands', 'postcode': '1234',
                          'town_or_city': 'Amsterdam', 'street_address1':
                          'Street', 'street_address2': '22', 'county':
                          'North'})
        self.assertTrue(form.is_valid())

    def test_correct_messsage_for_missing_name(self):
        form = OrderForm({'full_name': '', 'phone_number': '123456789',
                          'country': 'Netherlands', 'postcode': '1234',
                          'town_or_city': 'Amsterdam', 'street_address1':
                          'Street', 'street_address2': '22', 'county':
                          'North'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['full_name'],
                         [u'This field is required.'])

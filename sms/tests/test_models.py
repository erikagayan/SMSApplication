from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from sms.models import User


class UserModelTest(TestCase):
    def test_number_max_length(self):
        user = User(number='1234567890123456')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_number_unique(self):
        User.objects.create(number='123456789012345')
        with self.assertRaises(IntegrityError):
            User.objects.create(number='123456789012345')

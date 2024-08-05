from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from sms.models import User, List, SMS, Configuration


class UserModelTest(TestCase):
    def test_number_max_length(self):
        user = User(number="1234567890123456", name="John Doe")
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_number_unique(self):
        User.objects.create(number="123456789012345", name="John Doe")
        with self.assertRaises(IntegrityError):
            User.objects.create(number="123456789012345", name="Jane Smith")

    def test_name_max_length(self):
        user = User(number="1234567890", name="J" * 256)
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_create_user_with_valid_data(self):
        user = User.objects.create(number="1234567890", name="John Doe")
        self.assertEqual(user.number, "1234567890")
        self.assertEqual(user.name, "John Doe")


class ListModelTest(TestCase):
    def test_add_users_to_list(self):
        list_obj = List.objects.create(name="Test List")
        user1 = User.objects.create(number="1234567890")
        user2 = User.objects.create(number="0987654321")

        list_obj.users.add(user1, user2)

        # Check that users are added to the list
        self.assertIn(user1, list_obj.users.all())
        self.assertIn(user2, list_obj.users.all())

        # Checks that users have the list
        self.assertIn(list_obj, user1.lists.all())
        self.assertIn(list_obj, user2.lists.all())


class SMSModelTest(TestCase):
    def test_create_sms(self):
        sender = User.objects.create(number="1234567890")
        receiver = User.objects.create(number="0987654321")
        content = "Hello, this is a test message."

        sms = SMS.objects.create(
            sender=sender, receiver=receiver, content=content, timestamp=timezone.now()
        )

        self.assertEqual(sms.sender, sender)
        self.assertEqual(sms.receiver, receiver)
        self.assertEqual(sms.content, content)
        self.assertIsNotNone(sms.timestamp)


class ConfigurationModelTest(TestCase):
    def test_create_configuration(self):
        config = Configuration.objects.create(max_sms_per_hour=10)
        self.assertEqual(config.max_sms_per_hour, 10)

    def test_max_sms_per_hour_positive(self):
        config = Configuration(max_sms_per_hour=-1)
        with self.assertRaises(ValidationError):
            config.full_clean()  # Will check for PositiveIntegerField validation

        config.max_sms_per_hour = 10
        try:
            config.full_clean()  # Should pass as 10 is a positive integer
        except ValidationError:
            self.fail("full_clean() raised ValidationError unexpectedly!")

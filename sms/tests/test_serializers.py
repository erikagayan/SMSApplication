from django.test import TestCase
from rest_framework.exceptions import ValidationError
from sms.models import User, List
from sms.serializers import UserSerializer, ListSerializer


class UserSerializerTest(TestCase):
    def test_create_user(self):
        data = {'number': '1234567890', 'name': 'John Doe'}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.number, '1234567890')
        self.assertEqual(user.name, 'John Doe')

    def test_user_validation(self):
        data = {'number': '', 'name': 'John Doe'}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('number', serializer.errors)

        data = {'number': '1234567890', 'name': ''}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class ListSerializerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(number='1234567890', name='John Doe')
        self.user2 = User.objects.create(number='0987654321', name='Jane Smith')

    def test_create_list(self):
        data = {'name': 'Test List', 'users': [self.user1.id, self.user2.id], 'created_by': self.user1.id}
        serializer = ListSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        list_obj = serializer.save()
        self.assertEqual(list_obj.name, 'Test List')
        self.assertEqual(list_obj.created_by, self.user1)
        self.assertIn(self.user1, list_obj.users.all())
        self.assertIn(self.user2, list_obj.users.all())

    def test_list_validation(self):
        data = {'name': '', 'users': [self.user1.id, self.user2.id], 'created_by': self.user1.id}
        serializer = ListSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

        data = {'name': 'Test List', 'users': [], 'created_by': self.user1.id}
        serializer = ListSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # Empty list of users is valid

    def test_add_user_to_list(self):
        list_obj = List.objects.create(name='Test List', created_by=self.user1)
        data = {'name': 'Test List', 'users': [self.user1.id, self.user2.id], 'created_by': self.user1.id}
        serializer = ListSerializer(list_obj, data=data)
        self.assertTrue(serializer.is_valid())
        list_obj = serializer.save()
        self.assertIn(self.user1, list_obj.users.all())
        self.assertIn(self.user2, list_obj.users.all())

    def test_remove_user_from_list(self):
        list_obj = List.objects.create(name='Test List', created_by=self.user1)
        list_obj.users.add(self.user1, self.user2)
        data = {'name': 'Test List', 'users': [self.user1.id], 'created_by': self.user1.id}
        serializer = ListSerializer(list_obj, data=data)
        self.assertTrue(serializer.is_valid())
        list_obj = serializer.save()
        self.assertIn(self.user1, list_obj.users.all())
        self.assertNotIn(self.user2, list_obj.users.all())

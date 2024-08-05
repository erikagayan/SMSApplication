from sms.models import User, List, SMS
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "number", "name"]


class ListSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = List
        fields = ["id", "name", "users", "created_by"]


class SMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMS
        fields = ["id", "sender", "receiver", "content", "timestamp"]

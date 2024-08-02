from django.db import models


class User(models.Model):
    """Store user information"""

    number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name, self.number


class List(models.Model):
    """Lists of users. One list can contain many users."""

    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="lists")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_lists')

    def __str__(self):
        return self.name


class SMS(models.Model):
    """Stores SMS messages"""

    sender = models.ForeignKey(User, related_name="sent_sms", on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name="received_sms", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class Configuration(models.Model):
    """Stores configuration"""

    max_sms_per_hour = models.PositiveIntegerField()

    def __str__(self):
        return f"Max SMS per hour: {self.max_sms_per_hour}"

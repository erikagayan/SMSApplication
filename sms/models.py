from django.db import models


class User(models.Model):
    """Store user information"""

    number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)  # User name

    def __str__(self):
        return f"{self.name} ({self.number})"


class List(models.Model):
    """Lists of users. One list can contain many users."""

    name = models.CharField(max_length=255)  # List name
    users = models.ManyToManyField(User, related_name="lists")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_lists"
    )  # Who created the list

    def __str__(self):
        return self.name


class SMS(models.Model):
    """Stores SMS messages"""

    sender = models.ForeignKey(
        User, related_name="sent_sms", on_delete=models.CASCADE
    )  # Message sender
    receiver = models.ForeignKey(
        User, related_name="received_sms", on_delete=models.CASCADE  # Message receiver
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Date of sms

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    """Add indexes to improve performance (faster database search)"""

    class Meta:
        indexes = [
            models.Index(fields=["sender"]),
            models.Index(fields=["receiver"]),
        ]


class Configuration(models.Model):
    """Stores configuration"""

    max_sms_per_hour = models.PositiveIntegerField()

    def __str__(self):
        return f"Max SMS per hour: {self.max_sms_per_hour}"

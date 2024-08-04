# Generated by Django 5.0.7 on 2024-08-04 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sms", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="sms",
            index=models.Index(fields=["sender"], name="sms_sms_sender__bef70c_idx"),
        ),
        migrations.AddIndex(
            model_name="sms",
            index=models.Index(fields=["receiver"], name="sms_sms_receive_e9b24d_idx"),
        ),
    ]
# Generated by Django 4.2 on 2025-07-08 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_subscription_chat_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='category',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='phone',
        ),
    ]

# Generated by Django 4.2 on 2024-07-23 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_wallet_tokens_tokeninwallet_wallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tokeninwallet',
            name='wallet',
        ),
    ]

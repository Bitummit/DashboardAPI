# Generated by Django 4.2 on 2024-07-23 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_tokeninwallet_alter_wallet_tokens'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='tokens',
        ),
        migrations.AddField(
            model_name='tokeninwallet',
            name='wallet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to='api.wallet'),
        ),
    ]

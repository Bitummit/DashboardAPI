# Generated by Django 4.2 on 2024-08-14 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_delete_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=10, default=0, max_digits=20)),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('Canceled', 'Canceled')], default='Pending', max_length=9)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.tokeninwallet')),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outcoming_transactions', to=settings.AUTH_USER_MODEL)),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 5.1.6 on 2025-04-03 11:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_wallet_balance_alter_transaction_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificationmodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.CharField(blank=True, max_length=100, null=True)),
                ('notificationdate', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.usertable')),
            ],
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-26 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_balance_moneylog_errorlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='balance',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bot', to='backend.balance'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-09-03 00:21

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='confirmation_code',
            field=models.PositiveIntegerField(default=1, max_length=5, validators=[user.models.validate_min_length]),
            preserve_default=False,
        ),
    ]

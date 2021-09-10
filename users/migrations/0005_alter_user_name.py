# Generated by Django 3.2.7 on 2021-09-10 09:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(
                max_length=50, validators=[django.core.validators.MinLengthValidator(1)]
            ),
        ),
    ]

# Generated by Django 3.2.7 on 2021-09-15 07:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.PROTECT, to="users.role"
            ),
        ),
    ]

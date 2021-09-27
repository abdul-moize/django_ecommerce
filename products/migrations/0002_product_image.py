# Generated by Django 3.2.7 on 2021-09-24 14:59

from django.db import migrations, models

import products.models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(
                default="default_image.png", upload_to=products.models.image_path
            ),
        ),
    ]

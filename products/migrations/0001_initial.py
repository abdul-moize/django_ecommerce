# Generated by Django 3.2.7 on 2021-09-21 06:49

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Price is in PKR/Rs",
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Product Price",
                    ),
                ),
                (
                    "stock_quantity",
                    models.PositiveIntegerField(verbose_name="Product Quantity"),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=1000, verbose_name="Product Description"
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Product Name")),
                (
                    "created_by",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

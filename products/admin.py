"""
Admin settings for product app
"""
from django.contrib import admin

# Register your models here.
from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    """
    Admin representation of the Product model
    """

    # pylint: disable=no-member, protected-access
    model = Product
    all_fields = [field.name for field in Product._meta.get_fields()]
    list_display = all_fields

    list_filter = ["id", "name", "created_by"]
    readonly_fields = ["created_on", "updated_on", "created_by"]

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.created_by = request.user
        obj.save()


admin.site.register(Product, ProductAdmin)

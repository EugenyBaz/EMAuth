from django.contrib import admin

from catalog.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "price", "owner")
    list_filter = ("owner",)
    search_fields = ("name", "model", "owner__email")

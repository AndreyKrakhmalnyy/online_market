from django.contrib import admin
from goods.models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """Отвечает за регистрацию модели Categories в админке и отображает все категории товаров."""
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name"]

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    """Отвечает за регистрацию модели Products в админке, отображает все товары с дополнительными полями по фильтрации и поиску.
    """
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "quantity", "price", "discount"]
    search_fields = [
        "name",
    ]
    list_filter = ["name", "quantity", "discount"]
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
    ]

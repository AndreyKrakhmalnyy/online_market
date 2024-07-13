from django.contrib import admin
from carts.models import Cart

@admin.register(Cart)
class CartsAdmin(admin.ModelAdmin):
    """Отвечает за регистрацию модели в админке и отображает дополнительными полями по фильтрации.
        Также позволяет менять данные в корзине пользователей (inlines).
    """
    list_display = ["user_display", "product", "quantity", "created_timestamp"]
    list_filter = ["product", "created_timestamp"]
    
    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"
    
    user_display.short_description = "Пользователь"
    
class CartTablesAdmin(admin.TabularInline):
    model = Cart
    fields = "product", "quantity", "created_timestamp"
    search_fields = "product", "quantity", "created_timestamp"
    readonly_fields = ("created_timestamp",)
    extra = 1
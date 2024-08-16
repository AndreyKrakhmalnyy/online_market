from django.contrib import admin
from carts.admin import CartTablesAdmin
from orders.admin import OrderTableAdmin
from users.models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    """Отвечает за регистрацию модели User в админ панели, отображает всех пользователей с дополнительными полями по фильтрации.
        Также позволяет менять данные в корзине каждого пользователя (inlines).
    """
    list_display = ["username", "first_name", "last_name", "email", "is_staff"]
    list_filter = ["is_staff"]
    search_fields = ["username", "first_name", "last_name", "email",]
    inlines = [CartTablesAdmin, OrderTableAdmin,]
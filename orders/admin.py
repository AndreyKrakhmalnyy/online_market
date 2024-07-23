from django.contrib import admin
from orders.models import Order, OrderItem


class OrderItemTableAdmin(admin.TabularInline):
    model = OrderItem
    fields = ["name", "product", "price", "quantity"]
    search_fields = ["name", "product"]
    extra = 0
    
class OrderTableAdmin(admin.TabularInline):
    model = Order
    fields = ["id", "requires_delivery", "status", "payment_on_get", "is_paid", "created_timestamp"]
    search_fields = ["id"]
    readonly_fields = ["id", "requires_delivery", "status", "payment_on_get", "is_paid", "created_timestamp"]
    extra = 0    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "requires_delivery", "status", "payment_on_get", "is_paid", "created_timestamp"]
    list_filter = ["status", "requires_delivery", "payment_on_get", "is_paid"]
    search_fields = ["id"]
    readonly_fields = ["created_timestamp"]
    inlines = [OrderItemTableAdmin,]
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "name", "price", "quantity"]
    list_filter = ["id"]
    search_fields = ["order", "product", "name"]
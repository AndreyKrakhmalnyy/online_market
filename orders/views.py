from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


@login_required
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data['requires_delivery'] == "1" and not form.cleaned_data['delivery_address']:
                messages.warning(request, 'Введите адрес доставки!')
                return redirect('orders:create_order')
            else:
                try:
                    with transaction.atomic():
                        user = request.user
                        cart_items = Cart.objects.filter(user=user)
                        
                        if cart_items.exists():
                            order = Order.objects.create(
                                user=user,
                                phone_number=form.cleaned_data['phone_number'],
                                requires_delivery=form.cleaned_data['requires_delivery'],
                                delivery_address=form.cleaned_data['delivery_address'],
                                payment_on_get=form.cleaned_data['payment_on_get'],
                            )
                            
                            for cart_item in cart_items:
                                product = cart_item.product
                                name = cart_item.product.name
                                price = cart_item.product.discount_calculation()
                                quantity = cart_item.quantity
                                
                                try:
                                    if product.quantity < quantity:
                                        messages.warning(request, 'Недостаточное количество товара на складе!')
                                        return redirect('orders:create_order')
                                    
                                    OrderItem.objects.create(
                                        order=order,
                                        product=product,
                                        name=name,
                                        price=price,
                                        quantity=quantity,
                                    )
                                    product.quantity -= quantity
                                    product.save()
                                    
                                except ValidationError as e:
                                    messages.warning(request, str(e))
                                    return redirect('user:profile')
                            
                            cart_items.delete()
                            messages.success(request, 'Заказ оформлен!')
                            return redirect('user:profile')
                        
                except ValidationError as e:
                    messages.success(request, str(e))
                    return redirect('orders:create_order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        
        form = CreateOrderForm(initial=initial)
        
    context = {
        'title': 'Оформление заказа',
        'form': form,
        'order': True,
    }
    return render(request, "orders/create_order.html", context=context)

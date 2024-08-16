from django.http import JsonResponse
from django.views import View
from carts.mixins import CartMixin
from carts.models import Cart
from goods.models import Products


class CartAddView(CartMixin, View):
    def post(self, request):
        """Отвечает за добавление товаров в корзину как для авторизованного, 
            так и для анонимного пользователяей (с помощью сессионных ключей).
        """
        
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id=product_id)
        cart = self.get_cart(request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                product=product, quantity=1)
            
        response_data = {
            "message": "Товар добавлен в корзину",
            "cart_items_html": self.render_cart(request),
    }

        return JsonResponse(response_data)

class CartChangeView(CartMixin, View):
    def post(self, request):
        """Производит изменение количества товаров в корзине."""
        
        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)
        cart.quantity = request.POST.get("quantity")
        
        cart.save()

        updated_quantity = cart.quantity

        response_data = {
            "message": "Количество товара изменено",
            "cart_items_html": self.render_cart(request),
            "quantity": updated_quantity
        }

        return JsonResponse(response_data)

class CartRemoveView(CartMixin, View):
    def post(self, request):
        """Реализует функцию удаления любой позиции товара в корзине."""
        
        cart_id = request.POST.get("cart_id")
        cart = self.get_cart(request, cart_id=cart_id)
        cart.quantity = request.POST.get("quantity")
        
        cart.delete()
        quantity = cart.quantity
        response_data = {
            "message": "Товар удалён из корзины",
            "cart_items_html": self.render_cart(request),
            "quantity_deleted": quantity,
        }

        return JsonResponse(response_data)
from django.shortcuts import redirect, render
from carts.models import Cart
from goods.models import Products

def cart_add(request, product_slug: str):
    """Добавляет товар в корзину авторизованного пользователя.

        Если товар уже есть в корзине, то увеличивает его количество, иначе создаёт новую запись в корзине.

        Args:
            request: Запрос пользователя.
            product_slug: Slug товара.

        Attributes:
            product: Запрашиваемый объект из БД по его slug.
            
        Returns:
            HttpResponseRedirect: Перенаправление пользователя на предыдущую страницу.
    """
    product = Products.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
            
    return redirect(request.META["HTTP_REFERER"])    

def cart_change(request, product_slug):
    pass

def cart_remove(request, cart_id: int):
    """Удаляет товар по его id модели 'Cart' из корзины авторизованного пользователя и направляет его предыдущую страницу.
    
        Args:
            request: Запрос пользователя.
            cart_id: id товара.
    
        Attributes:
            cart: Запрашиваемый объект из БД по его id.
            
        Returns:
            HttpResponseRedirect: Перенаправление пользователя на предыдущую страницу.
    """
    
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect(request.META["HTTP_REFERER"]) 
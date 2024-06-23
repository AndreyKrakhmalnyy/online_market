from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from goods.models import Products


def product(request, product_slug):
    """Функция, отображающая шаблон product.html приложения goods.

    Параметры переменной 'context':
        product - информация о 'product_id' всех товаров из БД.
    """

    product = Products.objects.get(slug=product_slug)
    context = {"product": product}
    return render(request, "goods/product.html", context=context)


def catalog(request, category_slug):
    """Функция отображает шаблон 'catalog.html' сервиса 'goods' и возвращает информацию о товарах через переменную 'context'.

    Параметры переменной 'context':
        title - заголовок шаблона;
        goods - информация о всех товарах из БД.
    """
    page = request.GET.get('page', 1)
    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))
    context = {
        "title": "Home - Каталог", 
        "goods": current_page,
        "slug_url": category_slug,
    }

    if category_slug == 'all-goods':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))
        
    return render(request, "goods/catalog.html", context)
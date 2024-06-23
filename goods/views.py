from django.shortcuts import render
from goods.models import Products


def product(request, product_slug):
    """Функция, отображающая шаблон product.html приложения goods.

    Параметры переменной 'context':
        product - информация о 'product_id' всех товаров из БД.
    """

    product = Products.objects.get(slug=product_slug)
    context = {"product": product}
    return render(request, "goods/product.html", context=context)


def catalog(request):
    """Функция отображает шаблон 'catalog.html' приложения 'goods' и возвращает информацию о товарах через переменную 'context'.

    Параметры переменной 'context':
        title - заголовок шаблона;
        goods - информация о всех товарах из БД.
    """

    goods = Products.objects.all()
    context = {"title": "Home - Каталог", "goods": goods}
    return render(request, "goods/catalog.html", context)

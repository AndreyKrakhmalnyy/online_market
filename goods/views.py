from django.shortcuts import render
from goods.models import Products


def product(request):
    """Функция, отображающая шаблон product.html приложения goods."""
    return render(request, "goods/product.html")


def catalog(request):
    """Функция отображает шаблон 'catalog.html' приложения 'goods' и возвращает информацию о товарах через переменную 'context'.

    Параметры переменной 'context':
        title - заголовок шаблона;
        goods - информация о товаре, передаваемая из файла 'goods_list.py' в текущей директории.
    """
    goods = Products.objects.all()

    context = {"title": "Home - Каталог", "goods": goods}
    return render(request, "goods/catalog.html", context)

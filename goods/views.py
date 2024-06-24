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

    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)

    #Если 'slug' из таблицы 'Categories' равен 'all-goods', то отобразить все товары из БД, иначе отображает по выбранному значению 'slug'.
    if category_slug == "all-goods":
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    #Если товар со скидкой ('on_sale'=True), то отобразить те товары, у которых 'discount' больше нуля."""
    if on_sale:
        goods = Products.objects.filter(discount__gt=0)
        
    #Если 'order_by'=True, то есть если галочка в фильтрн сортировки указана и не равна 'default', то отсортировать товары)."""
    if order_by and order_by != "default":
        goods = Products.objects.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))
    context = {
        "title": "Home - Каталог",
        "goods": current_page,
        "slug_url": category_slug,
    }

    return render(request, "goods/catalog.html", context)

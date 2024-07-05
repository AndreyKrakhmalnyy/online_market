from typing import Any
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, render
from goods.models import Products
from goods.utils import q_search


def product(request, product_slug: str):
    """Отображает шаблон 'product.html' приложения 'goods'.

    Args:
        request: Запрос пользователя.
        product_slug: 'slug' товара.

    Attributes:
        product: Запрашиваемый объект товара из БД по его 'slug'.
        context: Словарь, содержащий объект товара для передачи в шаблон.

    Returns:
        HttpResponse: Ответ, отображающий шаблон 'goods/product.html' с контекстом, содержащим объект товара.
    """

    product: Products = Products.objects.get(slug=product_slug)
    context: dict[str, Products] = {"product": product}

    return render(request, "goods/product.html", context=context)


def catalog(request, category_slug: str = None) -> HttpResponse:
    """Отображает шаблон 'catalog.html' сервиса 'goods'.

    Обрабатывает GET-параметры запроса для фильтрации и сортировки товаров.

    Args:
        request: Запрос пользователя.
        category_slug: 'slug' категории (если задан).

    Attributes:
        page: Номер страницы для пагинации (по умолчанию 1).
        on_sale: Флаг, указывающий на то, нужно ли показывать только товары со скидкой (по умолчанию None).
        order_by: Критерий сортировки (по умолчанию None).
        query: Поисковый запрос (по умолчанию None).
        goods: QuerySet с товарами, отфильтрованными и отсортированными по параметрам запроса.
        paginator: Объект 'Paginator' для пагинации товаров.
        current_page: Текущая страница пагинации.
        context: Словарь, содержащий данные для шаблона 'catalog.html'.

    Returns:
        HttpResponse: Ответ, отображающий шаблон 'catalog.html' с контекстом фильтрации и пагинации.
    """
    page = request.GET.get("page", 1)
    on_sale = request.GET.get("on_sale", None)
    order_by = request.GET.get("order_by", None)
    query = request.GET.get("q", None)

    if category_slug == "all-goods":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = Products.objects.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = Products.objects.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))
    context: dict[str, Any] = {
        "title": "Home - Каталог",
        "goods": current_page,
        "slug_url": category_slug,
    }

    return render(request, "goods/catalog.html", context)

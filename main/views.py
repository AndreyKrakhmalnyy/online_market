from typing import Any
from django.shortcuts import render
from goods.models import Categories


def index(request):
    """Отображает шаблон и возвращает информацию о товарах.

    Args:
        request: Запрос пользователя.

    Attributes:
        categories: QuerySet со всеми категориями товаров.
        context (dict[str, Any]): Словарь, содержащий данные для шаблона 'main/index.html'.

    Returns:
        HttpResponse: Ответ, отображающий шаблон 'main/index.html' с контекстом, содержащим информацию о категориях.
    """
    
    categories = Categories.objects.all()
    
    context: dict[str, Any]  = {
        'title': 'Главная',
        'content': 'Добро пожаловать в магазин мебели HomeLand!',
        'categories': categories
    }
    return render(request, 'main/index.html', context)

def about(request):
    """Отображает шаблон и возвращает информацию о странице.

    Args:
        request: Запрос пользователя.

    Attributes:
        context (dict[str, Any]): Словарь, содержащий данные для шаблона 'main/about.html'.

    Returns:
        HttpResponse: Ответ, отображающий шаблон 'main/about.html' с контекстом, содержащим заголовок и контент страницы.
    """
    context: dict[str, Any] = {
        'title': 'Общая информация',
        'content': 'О нас',
    }
    return render(request, 'main/about.html', context)
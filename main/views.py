from django.shortcuts import render
from goods.models import Categories


def index(request):
    """Функция отображает шаблон 'catalog.html' приложения 'main' и возвращает информацию о товарах через переменную 'context'.

    Параметры переменной 'context':
        title - заголовок вкладки;
        goods - заголовок страницы.
    """
    
    categories = Categories.objects.all()
    
    context = {
        'title': 'Home - Главная',
        'content': 'Магазин мебели HOME',
        'categories': categories
    }
    return render(request, 'main/index.html', context)

def about(request):
    """Функция отображает шаблон 'catalog.html' приложения 'main' и возвращает информацию о товарах через переменную 'context'.

    Параметры переменной 'context':
        title - заголовок вкладки;
        goods - заголовок страницы.
    """
    
    context = {
        'title': 'Общая информация',
        'content': 'О нас',
    }
    return render(request, 'main/about.html', context)
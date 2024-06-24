from django import template
from django.utils.http import urlencode
from goods.models import Categories

register = template.Library()


@register.simple_tag()
def tag_categories():
    """
    Возвращает queryset всех объектов модели.
    
    Returns:
        QuerySet[Categories]: Список всех объектов модели Categories.
    """
    return Categories.objects.all()


@register.simple_tag(takes_context=True)
def change_parameters(context, **kwargs):
    """
    Добавляет возможность корректной подгрузки и обновления страниц в разделе пагинации шаблона,
    учитывая контекст.

    Args:
        context (dict): Текущий контекст запроса, включает в себя request.
        *kwargs: Ключ-значение пары, которые будут добавлены в GET-параметры запроса.

    Returns:
        str: Закодированная строка URL, которая включает обновленные GET-параметры.
    """
    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)

from django.db.models import Q, BaseManager
from goods.models import Products


def q_search(query: str) -> BaseManager[Products]:
    """Метод для поиска товара по его id.

    Args:
        query: str - cтрока, содержащая id товара.

    Returns:
        QuerySet - набор объектов Products, соответствующих заданному id,
            либо пустой QuerySet, если id не найден.
    """
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    keywords: list[str] = [word for word in query.split() if len(query) > 2]
    q_objects = Q()
    
    for token in keywords:
        q_objects |= Q(description__icontains=token)
        
    return Products.objects.filter(q_objects)

# def q_search_id(query: str):
#     """Метод для поиска товара по его id.

#     Args:
#         query (str): Строка, содержащая id товара.

#     Returns:
#         QuerySet: Набор объектов Products, соответствующих заданному id,
#         либо пустой QuerySet, если id не найден.

#     Raises:
#         ValueError: Если query-строка не содержит только целые числа или её длина больше 5 символов.
#     """
#     if query.isdigit() and len(query) <= 5:
#         return Products.objects.filter(id=int(query))
#     raise ValueError("The Query string must contain only integers and contain up to 5 inclusive.")

# def q_search_substring(query: str):
#     keywords = [word for word in query.split() if len(query) > 2]
#     q_objects = Q()
    
#     for token in keywords:
#         q_objects |= Q(description__icontains=token)
        
#     return Products.objects.filter(q_objects)




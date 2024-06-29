from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import QuerySet
from goods.models import Products


def q_search(query: str) -> QuerySet[Products]:
    """Метод для поиска товара по его id.

    Args:
        query: str - cтрока, содержащая id товара.

    Returns:
        QuerySet - набор объектов Products, соответствующих заданному id,
            либо пустой QuerySet, если id не найден, иначе искать по полям name и description с учётом регистра, окончаний и т.д.
    """
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))
    
    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    return Products.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank")




# Кастомный моиск с учётом регистра, но без учёта падежей, окончаний.
    # <return Products.objects.filter(id=int(query))>
    # keywords: list[str] = [word for word in query.split() if len(query) > 2] # list-генератор, который разбивает поисковой запрос по пробелам при условии количества слов больше 2
    # q_objects = Q() # Q() - для сложных логических запросов к БД, который позволяет комбинировать различные условия AND, OR и NOT
    
    # for token in keywords: # цикл, который перебирает слова списка
    #     q_objects |= Q(description__icontains=token) # проверяет наличие слова (in description) по условию или (|), то есть обращается к столбцу description и ищет все возможные совпадения по словам 
    #     q_objects |= Q(name__icontains=token) # проверка по названию товара (in name)
        
    # return Products.objects.filter(q_objects) # возвращает карточки с совпадающим описанием или именем




from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)
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

    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )
    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>",
        )
    )

    return result


# Кастомный моиск с учётом регистра, но без учёта падежей, окончаний.
# <return Products.objects.filter(id=int(query))>
# keywords: list[str] = [word for word in query.split() if len(query) > 2] # list-генератор, который разбивает поисковой запрос по пробелам при условии количества слов больше 2
# q_objects = Q() # Q() - для сложных логических запросов к БД, который позволяет комбинировать различные условия AND, OR и NOT

# for token in keywords: # цикл, который перебирает слова списка
#     q_objects |= Q(description__icontains=token) # проверяет наличие слова (in description) по условию или (|), то есть обращается к столбцу description и ищет все возможные совпадения по словам
#     q_objects |= Q(name__icontains=token) # проверка по названию товара (in name)

# return Products.objects.filter(q_objects) # возвращает карточки с совпадающим описанием или именем


# Текущий встроенный поиск django
# if query.isdigit() and len(query) <= 5:
#     return Products.objects.filter(id=int(query))

# vector = SearchVector("name", "description") - вектор поиска, который извлекает данные из переданных полей
# query = SearchQuery(query) - создаём объект, который будет использоваться для поиска записей из входящей строки query

# result = Products.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank") - указываем параметр rank с классом SearchRank,
# который будет оценить релевантность данных к входящей строке query в float, где 0.0 - нерелеватный результат

# Для исключения rank=0.0 применяет filter, в котором отбираем только те, у которых rank > 0 и сортируем rank в обратном порядке,
# то есть от более подходящих к менее

# result = result.objects.annotate(headline=SearchHeadline("name", query, start_sel='<span style="font-weight: bold">', stop_sel="</span>")).get()
# result = result.objects.annotate(headline=SearchHeadline("description", query, start_sel='<span style="font-weight: bold">', stop_sel="</span>")).get()

# return result

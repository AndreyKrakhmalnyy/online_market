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
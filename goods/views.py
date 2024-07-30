from django.db.models.base import Model as Model
from django.views.generic import DetailView, ListView
from goods.models import Products
from goods.utils import q_search
from django.http import Http404
# from django.shortcuts import redirect
# from django.urls import reverse
# from django.views.decorators.cache import cache_page
# from django.db.models.query import QuerySet
# from django.contrib import messages


class ProductView(DetailView):
    template_name = "goods/product.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"
    allow_empty = False
    
    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class CatalogView(ListView):
    queryset = Products.objects.all().order_by("-id")
    context_object_name = "goods"
    template_name = "goods/catalog.html"
    paginate_by = 3
    
    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if category_slug == "all-goods":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = super().get_queryset().filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = super().get_queryset().order_by(order_by)
        
        return goods
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Каталог"
        context['slug_url'] = self.kwargs.get("category_slug")
        return context
    





# def product(request, product_slug: str):
#     """Отображает шаблон 'product.html' приложения 'goods'.

#     Args:
#         request: Запрос пользователя.
#         product_slug (str): slug товара.

#     Attributes:
#         product: Запрашиваемый объект товара из БД по его slug.
#         context (dict[str, Products]): Словарь, содержащий объект товара для передачи в шаблон.

#     Returns:
#         HttpResponse: Ответ, отображающий шаблон 'goods/product.html' с контекстом, содержащим объект товара.
#     """

#     product: Products = Products.objects.get(slug=product_slug)
#     context: dict[str, Products] = {"product": product}

#     return render(request, "goods/product.html", context=context)

# def catalog(request, category_slug: str = None) -> HttpResponse:
#     """Отображает шаблон 'catalog.html' сервиса 'goods'.

#     Обрабатывает GET-параметры запроса для фильтрации и сортировки товаров.

#     Args:
#         request: Запрос пользователя.
#         category_slug: 'slug' категории (если задан).

#     Attributes:
#         page: Номер страницы для пагинации (по умолчанию 1).
#         on_sale: Флаг, указывающий на то, нужно ли показывать только товары со скидкой (по умолчанию None).
#         order_by: Критерий сортировки (по умолчанию None).
#         query: Поисковый запрос (по умолчанию None).
#         goods: QuerySet с товарами, отфильтрованными и отсортированными по параметрам запроса.
#         paginator: Объект 'Paginator' для пагинации товаров.
#         current_page: Текущая страница пагинации.
#         context (dict[str, Any]): Словарь, содержащий данные для шаблона 'catalog.html'.

#     Returns:
#         HttpResponse: Ответ, отображающий шаблон 'catalog.html' с контекстом фильтрации и пагинации.
#     """
    # page = request.GET.get("page", 1)
    # on_sale = request.GET.get("on_sale", None)
    # order_by = request.GET.get("order_by", None)
    # query = request.GET.get("q", None)

    # if category_slug == "all-goods":
    #     goods = Products.objects.all()
    # elif query:
    #     goods = q_search(query)
    # else:
    #     goods = Products.objects.filter(category__slug=category_slug)
    #     if not goods.exists():
    #         raise Http404()

    # if on_sale:
    #     goods = Products.objects.filter(discount__gt=0)

    # if order_by and order_by != "default":
    #     goods = Products.objects.order_by(order_by)

#     paginator = Paginator(goods, 3)
#     current_page = paginator.page(int(page))
#     context: dict[str, Any] = {
#         "title": "Каталог товаров",
#         "goods": current_page,
#         "slug_url": category_slug,
#     }

#     return render(request, "goods/catalog.html", context)

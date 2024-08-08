from django.db.models.base import Model as Model
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from goods.models import Products
from goods.utils import q_search
from django.http import Http404



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
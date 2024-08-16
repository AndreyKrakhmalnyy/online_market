from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
import markdown


class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['content'] = 'Добро пожаловать в интернет-магазин мебели Kitchenland!'
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs):
        """Читает файл 'main/descriptions/about.md', преобразует его в HTML-код с помощью markdown."""
        
        with open('main/descriptions/about.md', 'r', encoding='utf-8') as f:
            description = f.read()
            description_html = mark_safe(markdown.markdown(description))
            
        context = super().get_context_data(**kwargs)
        context['title'] = 'Общая информация'
        context['description'] = description_html
        
        return context

class DeliveryView(TemplateView):
    template_name = 'main/delivery.html'
    
    def get_context_data(self, **kwargs):
        """Читает файл 'main/descriptions/delivery.md', преобразует его в HTML-код с помощью markdown."""
        
        with open('main/descriptions/delivery.md', 'r', encoding='utf-8') as f:
            description = f.read()
            description_html = mark_safe(markdown.markdown(description))
            
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставка'
        context['description'] = description_html
        
        return context
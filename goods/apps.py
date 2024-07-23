from django.apps import AppConfig


class GoodsConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'goods'
    verbose_name: str = 'Товары'

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфигурация сервиса.

    Attributes:
        default_auto_field - указывает, какой тип поля использовать для автоматического генерирования первичных ключей в моделях приложения;
        name - имя приложения, которое используется в Django для идентификации приложения;
        verbose_name - отображаемое имя приложения в административной панели.
    """
    
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'users'
    verbose_name: str = 'Пользователи'
    
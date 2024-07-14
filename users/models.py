from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель User описывает модель пользователя от AbstractUser, которая содержит базовые поля."""
    
    image = models.ImageField(
        upload_to="users_images", blank=True, null=True, verbose_name="Аватар"
    )
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        """Класс для отображения названий таблицы в БД и названия модели на русском языке.

            Attributes:
                db_table (str): строка, содержит название таблицы в БД;
                verbose_name (str): строка, содержит название модели на русском языке в единственном числе;
                verbose_name_plural (str): строка, содержит название модели на русском языке во множественном числе.
        """

        db_table: str = "user"
        verbose_name: str = "Пользователя"
        verbose_name_plural: str = "Пользователи"

    def __str__(self) -> str:
        return self.username

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Модель User описывает модель пользователя от AbstractUser, которая содержит базовые поля.
    """

    image = models.ImageField(
        upload_to="users_images", blank=True, null=True, verbose_name="Аватар"
    )

    class Meta:
        """Класс для отображения названий таблицы в БД и названия модели на русском языке.

        Атрибуты:
            db_table - строка, содержит название таблицы в БД;
            verbose_name - строка, содержит название модели на русском языке в единственном числе;
            verbose_name_plural - строка, содержит название модели на русском языке во множественном числе.
        """

        db_table = "users"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username

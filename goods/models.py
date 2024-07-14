from django.db import models
from django.urls import reverse


class Categories(models.Model):
    """
    Модель представляет собой категорию товаров/услуг в интернет-магазине.

        Attributes:
            name (str): строка, содержит уникальное имя категории, не более 150 символов;
            slug (str): строка, содержит уникальный URL-адрес категории, не более 200 символов.
    """

    name = models.CharField(max_length=150, unique=True, verbose_name="Имя")
    slug = models.CharField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )

    class Meta:
        """Класс для отображения названий таблицы в БД и названия модели на русском языке.

            Attributes:
                db_table - строка, содержит название таблицы в БД;
                verbose_name - строка, содержит название модели на русском языке в единственном числе;
                verbose_name_plural - строка, содержит название модели на русском языке во множественном числе.
        """

        db_table = "category"
        verbose_name = "категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        """Отображает название товара в админке."""
        
        return self.name


class Products(models.Model):
    """
    Представляет собой модель для описания категории товаров/услуг.

        Attributes:
            name (str): содержит уникальное имя категории, не более 150 символов;
            slug (str): содержит уникальный URL-адрес категории, не более 200 символов;
            descripion (str): поле может быть пустым, содержит URL-адрес категории, неограниченное число символов;
            image - изображение, может отсутствовать;
            price (float): - отображает стоимость товара, не более 3 чисел после запятой;
            discount (float): - содержит скидку на товар, не более 3 чисел после запятой;
            quantity (int): положительное целое число, содержит количество товара;
            category: внешний ключ на модель 'Categories' с опцией 'CASCADE'.
    """

    name = models.CharField(max_length=150, unique=True, verbose_name="Имя")
    slug = models.CharField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="goods_images", blank=True, null=True, verbose_name="Изображение"
    )
    price = models.DecimalField(
        default=0, max_digits=7, decimal_places=0, verbose_name="Стоимость в рублях"
    )
    discount = models.DecimalField(
        blank=True,
        null=True,
        default=0,
        max_digits=3,
        decimal_places=0,
        verbose_name="Скидка в %",
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество в шт.")
    category = models.ForeignKey(
        to=Categories, on_delete=models.CASCADE, verbose_name="Категория"
    )

    class Meta:
        """
        Метаданные для модели.

            Attributes:
                db_table (str): имя таблицы в базе данных для этой модели;
                verbose_name (str): текстовое представление единственного экземпляра модели в административной панели;
                verbose_name_plural (str): текстовое представление множественного числа модели в административной панели;
                ordering
        """

        db_table: str = "product"
        verbose_name: str = "продукт"
        verbose_name_plural: str = "Продукты"
        ordering = ("id",)

    def __str__(self) -> str:
        """Отображает имя товара в админке."""
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    
    def display_id(self):
        """Отображает артикул товара на его карточке."""
        return f"Артикул товара - {self.id:005}"

    def display_quantity(self):
        """Отображающий количество товара на его карточке."""
        return f"Штук в наличии - {self.quantity}"

    def discount_calculation(self):
        """Рассчитывает стоимость товара со скидкой и без неё."""
        if self.discount:
            return round(self.price * (100 - self.discount) / 100)
        return self.price

from django.db import models
from django.urls import reverse


class Categories(models.Model):
    """Модель представляет собой категорию товаров/услуг в интернет-магазине."""

    name = models.CharField(max_length=150, unique=True, verbose_name="Имя")
    slug = models.CharField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )

    class Meta:

        db_table = "category"
        verbose_name = "категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Products(models.Model):
    """Представляет собой модель для описания категории товаров/услуг."""

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
        db_table: str = "product"
        verbose_name: str = "продукт"
        verbose_name_plural: str = "Продукты"
        ordering = ("id",)

    def __str__(self) -> str:
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
    


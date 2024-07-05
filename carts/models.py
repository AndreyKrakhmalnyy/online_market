from django.db import models
from goods.models import Products
from users.models import User


class CartQueryset(models.QuerySet):

    def total_price(self):
        """Рассчитывает итоговую стоимость всех добавленных в корзину позиций, итерируя queryset."""
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        """Рассчитывает итоговое количество всех добавленных в корзину позиций, итерируя queryset, если он не пустой,
        иначе возвращает 0.
        """

        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    sesion_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        """
        Метаданные для модели.

            Attributes:
                db_table - имя таблицы в базе данных для этой модели;
                verbose_name - текстовое представление единственного экземпляра модели в административной панели;
                verbose_name_plural - текстовое представление множественного числа модели в административной панели.
        """

        db_table: str = "cart"
        verbose_name: str = "Корзина"
        verbose_name_plural: str = "Корзина"
        
    objects = CartQueryset().as_manager()

    def products_price(self):
        """Рассчитывает стоимость товара (со скидкой и без) с учётом его количества."""
        return round(self.product.discount_calculation() * self.quantity, 2)

    def __str__(self) -> str:
        return f"Корзина пользователя {self.user.username} | Товар {self.product.name} | Количество {self.quantity}"

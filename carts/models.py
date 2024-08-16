from django.db import models
from goods.models import Products
from users.models import User


class CartQueryset(models.QuerySet):
    """Расширенный QuerySet для модели Cart, предоставляющий методы для
        вычисления общей стоимости и количества товаров в корзине."""

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
    """Модель для описания каждой корзины из набора товаров пользователя."""
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь")
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        db_table: str = "cart"
        verbose_name: str = "Корзина"
        verbose_name_plural: str = "Корзина"
        ordering = ("id",)
        
    objects = CartQueryset().as_manager()

    def products_price(self):
        """Рассчитывает стоимость товара (со скидкой и без) с учётом его количества."""
        return round(self.product.discount_calculation() * self.quantity, 2)

    def __str__(self):
        if self.user:
            return f"{self.user.last_name} {self.user.first_name}"
        return "Анонимный пользователь"


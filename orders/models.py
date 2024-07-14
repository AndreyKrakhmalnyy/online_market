from django.db import models
from goods.models import Products
from users.models import User


class OrderQueryset(models.QuerySet):

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


class Order(models.Model):
    """
    Представляет собой модель для описания заказа.

        Attributes:
            user (ForeignKey): внешний ключ на модель 'User' с опцией 'SET_DEFAULT' (если пользователь удаляется, заказ останется,
                но поле 'user' станет 'None'). Может быть пустым, в этом случае заказ не привязан к конкретному пользователю.
            created_timestamp (DateTimeField): дата и время создания заказа.
            phone_number (CharField): номер телефона покупателя.
            requires_delivery (BooleanField): флаг, указывающий, требуется ли доставка.
            delivery_address (BooleanField): флаг, указывающий, требуется ли ввод адреса доставки.
            payment_on_get (BooleanField): флаг, указывающий, оплачивается ли заказ при получении.
            is_paid (BooleanField): флаг, указывающий, оплачен ли заказ.
            status (CharField): статус заказа (например, 'В обработке', 'Отправлен', 'Доставлен').
    """

    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_DEFAULT,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        default=None,
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания заказа"
    )
    phone_number = models.CharField(max_length=10, verbose_name="Номер телефона")
    requires_delivery = models.BooleanField(
        default=False, verbose_name="Требуется доставка"
    )
    delivery_address = models.BooleanField(default=True, verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(
        default=False, verbose_name="Оплата при получении"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(
        max_length=50, default="В обработке", verbose_name="Статус заказа"
    )

    class Meta:
        """
        Метаданные для модели.

            Attributes:
                db_table - имя таблицы в базе данных для этой модели;
                verbose_name - текстовое представление единственного экземпляра модели в административной панели;
                verbose_name_plural - текстовое представление множественного числа модели в административной панели.
        """

        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        """Отображает номер заказа и имя покупателя в админке."""
        return f"Заказ № {self.pk} | Покупатель - {self.user.last_name} {self.user.first_name}"


class OrderItem(models.Model):
    """
    Представляет собой модель для описания товара в заказе.

        Attributes:
            order (ForeignKey): внешний ключ на модель 'Order' с опцией 'CASCADE' (если заказ удаляется, то и этот товар удаляется).
            product (ForeignKey): внешний ключ на модель 'Products' с опцией 'SET_DEFAULT' (если товар удаляется, то поле 'product'
                становится 'None'). Может быть пустым, в этом случае товар не привязан к конкретному товару (например, может быть услуга).
            name (CharField): название товара.
            price (DecimalField): стоимость товара в рублях (целое число).
            quantity (PositiveIntegerField): количество товара.
            created_timestamp (DateTimeField): дата и время добавления товара в заказ.
    """

    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(
        to=Products,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Товар",
        default=None,
    )
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(
        default=0, max_digits=7, decimal_places=0, verbose_name="Стоимость в рублях"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата продажи"
    )

    class Meta:
        """
        Метаданные для модели.

            Attributes:
                db_table - имя таблицы в базе данных для этой модели;
                verbose_name - текстовое представление единственного экземпляра модели в административной панели;
                verbose_name_plural - текстовое представление множественного числа модели в административной панели.
        """

        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderQueryset().as_manager()

    def products_price(self):
        """Рассчитывает стоимость товара (со скидкой и без) с учётом его количества."""

        return round(self.product.discount_calculation() * self.quantity, 2)

    def __str__(self):
        """Отображает название товара и id заказа в админке."""

        return f"Товар {self.name} | Заказ {self.order.pk}"

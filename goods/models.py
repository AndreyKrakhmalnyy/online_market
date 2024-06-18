from django.db import models


class Categories(models.Model):
    """
    Модель Categories представляет собой категорию товаров/услуг в интернет-магазине.

    Переменные:
        name - строка, содержит уникальное имя категории, не более 150 символов;
        slug - строка, содержит уникальный URL-адрес категории, не более 200 символов.
    """

    name = models.CharField(max_length=150, unique=True, verbose_name="Имя")
    slug = models.CharField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )

    class Meta:
        """Класс для отображения названий таблицы в БД и названия модели на русском языке.
        Атрибуты:
            db_table - строка, содержит название таблицы в БД;
            verbose_name - строка, содержит название модели на русском языке в единственном числе;
            verbose_name_plural - строка, содержит название модели на русском языке во множественном числе.
        """

        db_table = "category"
        verbose_name = "категорию"
        verbose_name_plural = "Категории"
        
    def __str__(self):
        return self.name

class Products(models.Model):
    """
    Модель Categories представляет собой категорию товаров/услуг в интернет-магазине.

    Переменные:
        name - строка, содержит уникальное имя категории, не более 150 символов;
        slug - строка, содержит уникальный URL-адрес категории, не более 200 символов;
        descripion - строка, может быть пустой, содержит URL-адрес категории, неограниченное число символов;
        image - изображение, может отсутствовать;
        price - число с плавающей точкой, содержит стоимость товара, не более 3 чисел после запятой;
        discount - число с плавающей точкой, содержит скидку на товар, не более 3 чисел после запятой;
        quantity - положительное целое число, содержит количество товара;
        category - внешний ключ на модель 'Categories' с опцией 'CASCADE'.
    """

    name = models.CharField(max_length=150, unique=True, verbose_name="Имя")
    slug = models.CharField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    descripion = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0, max_digits=7, decimal_places=0, verbose_name='Стоимость в рублях')
    discount = models.DecimalField(blank=True, null=True, default=0, max_digits=3, decimal_places=0, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        """Класс для отображения названий таблицы в БД и названия модели на русском языке.
        Атрибуты:
            db_table - содержит  название таблицы в БД;
            verbose_name - содержит название модели на русском языке в единственном числе;
            verbose_name_plural - содержит название модели на русском языке во множественном числе.
        """

        db_table = "product"
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"
        
    def __str__(self) -> str:
        return f'{self.name}, количество - {self.quantity} шт.'
    
    def display_id(self):
        return f'Артикул товара - {self.id:005}'

    def display_quantity(self):
        return f'Штук в наличии - {self.quantity}' 
    
    def discount_calculation(self):
        if self.discount:
            return round(self.price * (100 - self.discount)/100)
        return self.price
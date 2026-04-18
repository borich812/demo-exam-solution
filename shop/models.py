from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Profile(models.Model):
    ROLE_GUEST = 'guest'
    ROLE_CLIENT = 'client'
    ROLE_MANAGER = 'manager'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_CLIENT, 'Авторизованный клиент'),
        (ROLE_MANAGER, 'Менеджер'),
        (ROLE_ADMIN, 'Администратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self) -> str:
        return self.full_name


class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class CakeType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    article = models.CharField('Артикул', max_length=20, primary_key=True)
    name = models.CharField('Наименование товара', max_length=255)
    unit = models.CharField('Единица измерения', max_length=50, default='шт.')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='products')
    cake_type = models.ForeignKey(CakeType, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    discount = models.PositiveSmallIntegerField('Действующая скидка', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stock = models.PositiveIntegerField('Количество на складе', default=0)
    description = models.TextField('Описание товара', blank=True)
    image = models.CharField('Путь к фото', max_length=255, blank=True)
    related_products = models.ManyToManyField('self', symmetrical=False, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.article} — {self.name}'

    @property
    def final_price(self) -> Decimal:
        return self.price * (Decimal(100) - Decimal(self.discount)) / Decimal(100)


class PickupPoint(models.Model):
    address = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.address


class OrderStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='orders')
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.PROTECT, related_name='orders')
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, related_name='orders')
    order_date = models.DateField('Дата заказа')
    delivery_date = models.DateField('Дата выдачи')
    pickup_code = models.CharField('Код получения', max_length=20)

    class Meta:
        ordering = ['-order_date', 'id']

    def __str__(self) -> str:
        return f'Заказ №{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self) -> str:
        return f'{self.order} / {self.product}'

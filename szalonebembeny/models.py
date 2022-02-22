from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    votes = models.IntegerField(default=0)
    score = models.DecimalField(max_digits=3, decimal_places=1, default=-1)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=9)
    address = models.CharField(max_length=128)
    liked_products = models.ManyToManyField(Product)

    def __str__(self):
        return f'Profil {self.user.username}'


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f'Komentarz {self.user.username} dla produktu {self.product.name}'


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProducts')

    def __str__(self):
        return f'Koszyk {self.user.username}'


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.amount} {self.product.name} w koszyku {self.cart.user.username}'


STATES = {
    (1, 'Zamówione'),
    (2, 'Opłacone'),
    (3, 'Wysłane'),
    (4, 'Odebrane')
}

DELIVER_METHODS = {
    ('paczkomat', 'Paczkomat Inpost'),
    ('poczta', 'PocztaPolska'),
    ('DPD', 'Kurier DPD')
}

PAYMENT_METHODS = {
    ('przelew', 'Przelew interentowy'),
    ('pobranie', 'Za pobraniem'),
    ('BLIK', 'Płatność BLIK')
}


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProducts')
    date = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=STATES, default=1)
    address = models.CharField(max_length=128)
    deliver_method = models.CharField(choices=DELIVER_METHODS, max_length=32)
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=32)
    full_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Zamówienie {self.user.username} z {self.date}'


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.amount} {self.product.name} w zamówieniu {self.order.user.username} z dnia {self.order.date}'

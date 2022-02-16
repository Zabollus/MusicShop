from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    stock = models.IntegerField()
    votes = models.IntegerField()
    score = models.DecimalField(max_digits=3, decimal_places=1)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=9)
    address = models.CharField(max_length=128)
    liked_products = models.ManyToManyField(Product)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=3, decimal_places=1)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartProducts')


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField()


STATES = {
    (1, 'Zamówione'),
    (2, 'Opłacone'),
    (3, 'Wysłane'),
    (4, 'Odebrane')
}


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProducts')
    date = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=STATES)


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.IntegerField()

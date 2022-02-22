from django.contrib import admin
from szalonebembeny.models import Product, Category, Profile, Comment, Cart, CartProducts, Order, OrderProducts
# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartProducts)
admin.site.register(Order)
admin.site.register(OrderProducts)

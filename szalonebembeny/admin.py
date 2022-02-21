from django.contrib import admin
from szalonebembeny.models import Product, Category, Profile, Comment, Cart, CartProducts
# Register your models here.


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartProducts)

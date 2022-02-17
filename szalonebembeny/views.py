from django.shortcuts import render
from django.views import View
from django.shortcuts import render
from szalonebembeny.models import Product, Category

# Create your views here.


class LandingPageView(View):
    def get(self, request):
        return render(request, 'index.html')


class ProductsView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products.html', {'products': products})


class CategoriesView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'categories.html', {'categories': categories})

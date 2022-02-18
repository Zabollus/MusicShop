from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from szalonebembeny.models import Product, Category

# Create your views here.


class LandingPageView(View):
    def get(self, request):
        products_by_score = Product.objects.all().order_by('score')
        return render(request, 'index.html', {'products': products_by_score})


class ProductsView(View):
    def get(self, request):
        products = Product.objects.all()
        title = 'Wszystkie produkty'
        return render(request, 'products.html', {'products': products, 'title': title})


class CategoriesView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'categories.html', {'categories': categories})


class ProductsInCategory(View):
    def get(self, request, id):
        products = Product.objects.all().filter(category_id=id)
        title = f'Produkty z kategorii {Category.objects.get(id=id).name}'
        return render(request, 'products.html', {'products': products, 'title': title})


class ProductAdd(CreateView):
    model = Product
    fields = 'name', 'description', 'category', 'price', 'stock'
    success_url = '/products/'


class ProductModify(UpdateView):
    model = Product
    fields = 'name', 'description', 'category', 'price', 'stock'
    success_url = '/products/'


class ProductDelete(DeleteView):
    model = Product
    success_url = '/products/'


class CategoryAdd(CreateView):
    model = Category
    fields = '__all__'
    success_url = '/categories/'


class CategoryModify(UpdateView):
    model = Category
    fields = '__all__'
    success_url = '/categories/'


class CategoryDelete(DeleteView):
    model = Category
    success_url = '/categories/'

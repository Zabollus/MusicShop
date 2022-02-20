from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from szalonebembeny.models import Product, Category, Profile
from szalonebembeny.forms import ProductAddForm, RegisterForm, LoginForm, ResetPasswordForm
from django.contrib.auth.mixins import PermissionRequiredMixin


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


class ProductAdd(PermissionRequiredMixin, View):
    permission_required = 'szalonebembeny.add_product'

    def get(self, request):
        form = ProductAddForm()
        return render(request, "szalonebembeny/product_form.html", {'form': form})

    def post(self, request):
        form = ProductAddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            stock = form.cleaned_data['stock']
            slug = name.replace(' ', '_').lower().replace('ą', 'a').replace('ę', 'e').replace('ó', 'o'). \
                replace('ć', 'c').replace('ń', 'n').replace('ł', 'l').replace('ż', 'z').replace('ź', 'z')
            Product.objects.create(name=name, slug=slug, description=description,
                                   category=category, price=price, stock=stock)
            return redirect('/products')
        else:
            return render(request, "szalonebembeny/product_form.html", {'form': form})


class ProductModify(PermissionRequiredMixin, UpdateView):
    permission_required = 'szalonebembeny.change_product'
    model = Product
    fields = 'name', 'description', 'category', 'price', 'stock'
    success_url = '/products/'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'szalonebembeny.delete_product'
    model = Product
    success_url = '/products/'


class CategoryAdd(PermissionRequiredMixin, CreateView):
    permission_required = 'szalonebembeny.add_category'
    model = Category
    fields = '__all__'
    success_url = '/categories/'


class CategoryModify(PermissionRequiredMixin, UpdateView):
    permission_required = 'szalonebembeny.change_category'
    model = Category
    fields = '__all__'
    success_url = '/categories/'


class CategoryDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'szalonebembeny.delete_category'
    model = Category
    success_url = '/categories/'


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        title = 'Rejestracja'
        button = 'Utwórz'
        return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['pass1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            Profile.objects.create(
                user=u,
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )
            login(request, u)
            return redirect('/')
        else:
            title = 'Rejestracja'
            button = 'Utwórz'
            return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        title = 'Logowanie'
        button = 'Zaloguj'
        return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_login, password=user_password)
            if user is None:
                title = 'Logowanie'
                button = 'Zaloguj'
                return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})
            else:
                login(request, user)
                return redirect('/')
        else:
            title = 'Logowanie'
            button = 'Zaloguj'
            return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class ResetPasswordView(View):
    def get(self, request, id):
        form = ResetPasswordForm()
        title = 'Resetowanie hasła'
        button = 'Resetuj'
        return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})

    def post(self, request, id):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            u = User.objects.get(id=id)
            u.set_password(form.cleaned_data['pass1'])
            u.save()
            return redirect('/')
        else:
            title = 'Resetowanie hasła'
            button = 'Resetuj'
            return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})

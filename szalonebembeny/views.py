from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from szalonebembeny.models import Product, Category, Profile, Cart, CartProducts, Comment
from szalonebembeny.forms import ProductAddForm, RegisterForm, LoginForm, ResetPasswordForm, CommentAddForm, ProfileEditForm
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.


class LandingPageView(View):
    def get(self, request):
        products_by_score = Product.objects.all().order_by('-score')
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
            Cart.objects.create(user=u)
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
    def get(self, request):
        form = ResetPasswordForm()
        title = 'Resetowanie hasła'
        button = 'Resetuj'
        return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            u = request.user
            u.set_password(form.cleaned_data['pass1'])
            u.save()
            return redirect('/')
        else:
            title = 'Resetowanie hasła'
            button = 'Resetuj'
            return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})


class ProductDetailsView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        liked_products = Profile.objects.get(user=request.user).liked_products.all()
        product_in_liked = product in liked_products
        comments = Comment.objects.all().filter(product=product)
        return render(request, 'product-details.html', {
            'product': product, 'product_in_like': product_in_liked, 'comments': comments
        })

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        comments = Comment.objects.all().filter(product=product)
        user = request.user
        if request.POST.get('like') == 'like':
            user_profile = Profile.objects.get(user=user)
            user_profile.liked_products.add(product)
            liked_products = Profile.objects.get(user=user).liked_products.all()
            product_in_liked = product in liked_products
            product.votes += 1
            product.save()
            return render(request, 'product-details.html', {
                'product': product, 'product_in_like': product_in_liked, 'comments': comments
            })
        elif request.POST.get('unlike') == 'unlike':
            user_profile = Profile.objects.get(user=user)
            user_profile.liked_products.remove(product)
            liked_products = Profile.objects.get(user=user).liked_products.all()
            product_in_liked = product in liked_products
            product.votes -= 1
            product.save()
            return render(request, 'product-details.html', {
                'product': product, 'product_in_like': product_in_liked, 'comments': comments
            })
        elif request.POST.get('cart') == 'cart':
            liked_products = Profile.objects.get(user=user).liked_products.all()
            product_in_liked = product in liked_products
            cart = Cart.objects.get(user=user)
            if CartProducts.objects.filter(cart=cart, product=product).exists():
                cp = CartProducts.objects.get(cart=cart, product=product)
                cp.amount += 1
                cp.save()
            else:
                CartProducts.objects.create(cart=cart, product=product, amount=1)
            return render(request, 'product-details.html', {
                'product': product, 'product_in_like': product_in_liked, 'comments': comments
            })


class CommentAddView(View):
    def get(self, request, slug):
        form = CommentAddForm()
        title = 'Dodawanie komentarza'
        button = 'Dodaj'
        return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})

    def post(self, request, slug):
        form = CommentAddForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(slug=slug)
            content = form.cleaned_data['content']
            score = form.cleaned_data['score']
            Comment.objects.create(
                user=request.user,
                product=product,
                content=content,
                score=score
            )
            comments = Comment.objects.all().filter(product=product)
            suma = 0
            for comment in comments:
                suma += comment.score
            avg = suma/len(comments)
            product.score = avg
            product.save()
            return redirect('product', slug=product.slug)
        else:
            title = 'Dodawanie komentarza'
            button = 'Dodaj'
            return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})


class CartView(View):
    def get(self, request):
        emptycart = ''
        cart = Cart.objects.get(user=request.user)
        full_cost = 0
        for element in cart.cartproducts_set.all():
            full_cost += element.amount * element.product.price
        if len(cart.products.all()) == 0:
            emptycart = ' jest pusty'
        return render(request, 'cart.html', {'cart': cart, 'emptycart': emptycart, 'full_cost': full_cost})


class ProductDeleteFromCartView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        user = request.user
        cart = Cart.objects.get(user=user)
        cp = CartProducts.objects.get(cart=cart, product=product)
        if cp.amount == 1:
            cp.delete()
        else:
            cp.amount -= 1
            cp.save()
        return redirect('cart')


class ProfileEditView(View):
    def get(self, request):
        user = request.user
        profil = Profile.objects.get(user=user)
        form = ProfileEditForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': profil.phone_number,
            'address': profil.address
        })
        title = 'Edycja profilu'
        button = 'Edytuj'
        return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})

    def post(self, request):
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            user = request.user
            profil = Profile.objects.get(user=user)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            profil.phone_number = form.cleaned_data['phone_number']
            profil.address = form.cleaned_data['address']
            user.save()
            profil.save()
            return redirect('/')
        else:
            title = 'Edycja profilu'
            button = 'Edytuj'
            return render(request, 'basic_form.html', {'form': form, 'title': title, 'button': button})

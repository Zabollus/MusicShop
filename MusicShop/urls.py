"""MusicShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from szalonebembeny.views import LandingPageView, ProductsView, CategoriesView, ProductsInCategory, ProductAdd, \
    CategoryAdd, ProductModify, CategoryModify, ProductDelete, CategoryDelete, LoginView, LogoutView, RegisterView, \
    ResetPasswordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='main'),
    path('products/', ProductsView.as_view(), name='products'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('productscategory/<int:id>', ProductsInCategory.as_view(), name='category-products'),
    path('product_add/', ProductAdd.as_view(), name='product-add'),
    path('category_add/', CategoryAdd.as_view(), name='category-add'),
    path('product/<slug>/edit/', ProductModify.as_view(), name='product-edit'),
    path('category/<int:pk>/edit/', CategoryModify.as_view(), name='category-edit'),
    path('product/<slug>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('category/<int:pk>/delete/', CategoryDelete.as_view(), name='category-delete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset_password/<int:id>/', ResetPasswordView.as_view(), name='reset-password')
]

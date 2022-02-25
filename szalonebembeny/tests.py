from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from szalonebembeny.models import Category, Product, Profile
import pytest


@pytest.mark.django_db
def test_sort_landingpageview(client, six_products_two_categories):
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'][0].score == 10.0
    assert response.context['products'][1].score == 9.0
    assert response.context['products'][2].score == 8.0
    assert response.context['products'][3].score == 7.5
    assert response.context['products'][4].score == 6.0


@pytest.mark.django_db
def test_len_products_landingpageview(client, six_products_two_categories):
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'].count() == 5


@pytest.mark.django_db
def test_search_products(client, six_products_two_categories):
    url = reverse('search')
    dct = {'search': 'gitara'}
    response = client.post(url, dct)
    assert response.status_code == 200
    assert response.context['products'].count() == 3
    assert response.context['categories'].count() == 0


@pytest.mark.django_db
def test_search_categories(client, six_products_two_categories):
    url = reverse('search')
    dct = {'search': 'instrumenty'}
    response = client.post(url, dct)
    assert response.status_code == 200
    assert response.context['products'].count() == 0
    assert response.context['categories'].count() == 2


@pytest.mark.django_db
def test_search_nothing(client, six_products_two_categories):
    url = reverse('search')
    dct = {'search': 'nic'}
    response = client.post(url, dct)
    assert response.status_code == 200
    assert response.context['products'].count() == 0
    assert response.context['categories'].count() == 0


@pytest.mark.django_db
def test_all_products_len(client, six_products_two_categories):
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'].count() == 6


@pytest.mark.django_db
def test_all_products_sort(client, six_products_two_categories):
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'][0].category.name == 'Instrumenty dęte'
    assert response.context['products'][1].category.name == 'Instrumenty dęte'
    assert response.context['products'][2].category.name == 'Instrumenty strunowe'
    assert response.context['products'][5].category.name == 'Instrumenty strunowe'


@pytest.mark.django_db
def test_all_categories_len(client, six_products_two_categories):
    url = reverse('categories')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['categories'].count() == 2


@pytest.mark.django_db
def test_all_categories_sort(client, six_products_two_categories):
    url = reverse('categories')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['categories'][0].name == 'Instrumenty dęte'
    assert response.context['categories'][1].name == 'Instrumenty strunowe'


@pytest.mark.django_db
def test_products_in_category_len(client, six_products_two_categories):
    category = Category.objects.get(name='Instrumenty strunowe')
    url = reverse('category-products', args=[category.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'].count() == 4


@pytest.mark.django_db
def test_products_in_category_name(client, six_products_two_categories):
    category = Category.objects.get(name='Instrumenty strunowe')
    url = reverse('category-products', args=[category.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'][0].category.name == 'Instrumenty strunowe'
    assert response.context['title'] == 'Produkty z kategorii Instrumenty strunowe'


@pytest.mark.django_db
def test_product_add_get(client, user_worker):
    url = reverse('product-add')
    client.force_login(user_worker)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_add_get_no_permission(client, normal_user):
    url = reverse('product-add')
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_product_add(client, user_worker, example_category):
    url = reverse('product-add')
    client.force_login(user_worker)
    dct = {
        'name': 'Kazoo',
        'description': 'Małe do dmuchania',
        'category': example_category.id,
        'price': 200.00,
        'stock': 20,
    }
    client.post(url, dct)
    assert Product.objects.get(**dct)


@pytest.mark.django_db
def test_product_modify_get(client, user_worker, example_product):
    url = reverse('product-edit', args=[example_product.slug])
    client.force_login(user_worker)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_modify_get_no_permission(client, normal_user, example_product):
    url = reverse('product-edit', args=[example_product.slug])
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_product_modify(client, user_worker, example_product, example_category):
    url = reverse('product-edit', args=[example_product.slug])
    client.force_login(user_worker)
    dct = {
        'name': 'test1',
        'description': 'test1',
        'category': example_category.id,
        'price': 2000.00,
        'stock': 20
    }
    client.post(url, dct)
    assert Product.objects.get(**dct)


@pytest.mark.django_db
def test_product_delete_get(client, user_worker, example_product):
    url = reverse('product-delete', args=[example_product.slug])
    client.force_login(user_worker)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_delete_get_no_permission(client, normal_user, example_product):
    url = reverse('product-delete', args=[example_product.slug])
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_product_delete(client, user_worker, example_product):
    url = reverse('product-delete', args=[example_product.slug])
    client.force_login(user_worker)
    dct = {'confirmation': 'tak'}
    client.post(url, dct)
    assert Product.objects.all().first() is None


@pytest.mark.django_db
def test_category_add_get(client, user_worker):
    url = reverse('category-add')
    client.force_login(user_worker)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_add_get_no_permission(client, normal_user):
    url = reverse('category-add')
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_category_add(client, user_worker):
    url = reverse('category-add')
    client.force_login(user_worker)
    dtc = {
        'name': 'test',
        'description': 'test'
    }
    client.post(url, dtc)
    assert Category.objects.get(**dtc)


@pytest.mark.django_db
def test_category_modify_get(client, user_worker, example_category):
    url = reverse('category-edit', args=[example_category.pk])
    client.force_login(user_worker)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_modify_get_no_permission(client, normal_user, example_category):
    url = reverse('category-edit', args=[example_category.pk])
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_category_modify(client, user_worker, example_category):
    url = reverse('category-edit', args=[example_category.pk])
    client.force_login(user_worker)
    dct = {
        'name': 'test1',
        'description': 'test1'
    }
    client.post(url, dct)
    assert Category.objects.get(**dct)


@pytest.mark.django_db
def test_category_delete_get(client, user_worker, example_category):
    url = reverse('category-delete', args=[example_category.pk])
    client.force_login(user_worker)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_category_delete_get_no_permission(client, normal_user, example_category):
    url = reverse('category-delete', args=[example_category.pk])
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_category_delete(client, user_worker, example_category):
    url = reverse('category-delete', args=[example_category.pk])
    client.force_login(user_worker)
    dct = {'confirmation': 'tak'}
    client.post(url, dct)
    assert Category.objects.all().first() is None


@pytest.mark.django_db
def test_register_get(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register(client):
    url = reverse('register')
    dct = {
        'username': 'test',
        'pass1': '12345',
        'pass2': '12345',
        'first_name': 'Jan',
        'last_name': 'Kowalski',
        'email': 'test@test.pl',
        'phone_number': '123456789',
        'address': 'Testowa 1 Testowo'
    }
    client.post(url, dct)
    assert User.objects.all().first().username == 'test'
    assert Profile.objects.all().first().phone_number == '123456789'


@pytest.mark.django_db
def test_register_wrong_password(client):
    url = reverse('register')
    dct = {
        'username': 'test',
        'pass1': '12345',
        'pass2': '123456',
        'first_name': 'Jan',
        'last_name': 'Kowalski',
        'email': 'test@test.pl',
        'phone_number': '123456789',
        'address': 'Testowa 1 Testowo'
    }
    client.post(url, dct)
    assert User.objects.all().first() is None
    assert Profile.objects.all().first() is None


@pytest.mark.django_db
def test_login_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login(client, normal_user):
    url = reverse('login')
    dct = {
        'login': 'Test',
        'password': '1234'
    }
    response = client.post(url, dct)
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_logout(client, normal_user):
    url = reverse('logout')
    response = client.get(url)
    assert not response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_logout_no_user(client):
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_reset_password(client, normal_user):
    url = reverse('reset-password')
    dct = {
        'pass1': '12345',
        'pass2': '12345'
    }
    client.post(url, dct)
    client.login(username='Test', password='12345')
    response = client.get('/')
    assert response.wsgi_request.user.is_authenticated

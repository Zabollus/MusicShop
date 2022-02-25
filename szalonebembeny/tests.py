from django.test import TestCase
from django.urls import reverse
from szalonebembeny.models import Category, Product
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
def test_category_modify(client, user_worker, example_category):
    url = reverse('category-edit', args=[example_category.pk])
    client.force_login(user_worker)
    dct = {
        'name': 'test1',
        'description': 'test1'
    }
    client.post(url, dct)
    assert Category.objects.get(**dct)
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from szalonebembeny.models import Category, Product, Profile, CartProducts, Comment, Order, OrderProducts
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
    client.force_login(normal_user)
    dct = {
        'pass1': '12345',
        'pass2': '12345'
    }
    response = client.post(url, dct)
    client.login(username='Test', password='12345')
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_reset_password_get(client, normal_user):
    url = reverse('reset-password')
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_reset_password_no_user(client):
    url = reverse('reset-password')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_product_details(client, example_product, example_comment):
    url = reverse('product', args=[example_product.slug])
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['product'].name == 'Gitara elektryczna'
    assert response.context['product'].description == 'Gitara wymagająca wzmacniacza i prądu'
    assert response.context['product'].price == 1000
    assert response.context['product'].stock == 10
    assert response.context['comments'].count() == 1


@pytest.mark.django_db
def test_product_details_like(client, example_product, normal_user, normal_user_profile):
    url = reverse('product', args=[example_product.slug])
    client.force_login(normal_user)
    dct = {
        'like': 'like'
    }
    client.post(url, dct)
    assert example_product in Profile.objects.get(user=normal_user).liked_products.all()


@pytest.mark.django_db
def test_product_details_cart(client, example_product, normal_user, normal_user_profile, normal_user_cart):
    url = reverse('product', args=[example_product.slug])
    client.force_login(normal_user)
    dct = {
        'cart': 'cart'
    }
    client.post(url, dct)
    assert CartProducts.objects.all().first().product == example_product


@pytest.mark.django_db
def test_comment_add_no_user(client, example_product):
    url = reverse('comment-add', args=[example_product.slug])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_comment_add_get(client, normal_user, example_product):
    url = reverse('comment-add', args=[example_product.slug])
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_add(client, example_product, normal_user):
    url = reverse('comment-add', args=[example_product.slug])
    client.force_login(normal_user)
    dct = {
        'content': 'super',
        'score': 9.0
    }
    client.post(url, dct)
    assert Comment.objects.get(**dct)


@pytest.mark.django_db
def test_comment_edit_no_user(client, example_product):
    url = reverse('comment-edit', args=[example_product.slug])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_comment_edit_get(client, normal_user, example_product, example_comment):
    url = reverse('comment-edit', args=[example_product.slug])
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_edit(client, normal_user, example_product, example_comment):
    url = reverse('comment-edit', args=[example_product.slug])
    client.force_login(normal_user)
    dct = {
        'content': 'test',
        'score': 10.0
    }
    client.post(url, dct)
    assert Comment.objects.get(**dct)


@pytest.mark.django_db
def test_cart_get_no_user(client):
    url = reverse('cart')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_cart_get(client, normal_user, example_cartproduct):
    url = reverse('cart')
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['cart'].cartproducts_set.all().count() == 1
    assert response.context['full_cost'] == 1000


@pytest.mark.django_db
def test_cart_add(client, normal_user, example_cartproduct, example_product):
    url = reverse('cart')
    client.force_login(normal_user)
    dct = {
        'add': '+1',
        'product_id': example_product.id
    }
    client.post(url, dct)
    assert CartProducts.objects.all().first().amount == 2
    assert Product.objects.all().first().stock == 9


@pytest.mark.django_db
def test_cart_sub(client, normal_user, example_cartproduct, example_product):
    url = reverse('cart')
    client.force_login(normal_user)
    dct = {
        'sub': '-1',
        'product_id': example_product.id
    }
    client.post(url, dct)
    assert CartProducts.objects.all().first().amount == 0
    assert Product.objects.all().first().stock == 11


@pytest.mark.django_db
def test_product_delete_from_cart_get_no_user(client, example_product):
    url = reverse('cart-product-delete', args=[example_product.slug])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_product_delete_from_cart_get(client, normal_user, example_product, example_cartproduct):
    url = reverse('cart-product-delete', args=[example_product.slug])
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('cart'))
    assert CartProducts.objects.all().first() is None


@pytest.mark.django_db
def test_profile_edit_get_no_user(client):
    url = reverse('profile-edit')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_profile_edit_get(client, normal_user, normal_user_profile):
    url = reverse('profile-edit')
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_edit(client, normal_user, normal_user_profile):
    url = reverse('profile-edit')
    client.force_login(normal_user)
    dct = {
        'first_name': 'Paweł',
        'last_name': 'Nowak',
        'email': 'abc@abc.com',
        'phone_number': '987654321',
        'address': 'Street 2'
    }
    client.post(url, dct)
    u = User.objects.all().first()
    p = Profile.objects.all().first()
    assert u.first_name == 'Paweł'
    assert u.last_name == 'Nowak'
    assert u.email == 'abc@abc.com'
    assert p.phone_number == '987654321'
    assert p.address == 'Street 2'


@pytest.mark.django_db
def test_order_add_get_no_user(client):
    url = reverse('order_add')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_order_add_get(client, normal_user, normal_user_profile, normal_user_cart, example_cartproduct):
    url = reverse('order_add')
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['full_cost'] == 1000


@pytest.mark.django_db
def test_order_add(client, normal_user, normal_user_profile, normal_user_cart, example_cartproduct):
    url = reverse('order_add')
    client.force_login(normal_user)
    dct = {
        'address': 'Testowa 12',
        'deliver_method': 'paczkomat',
        'payment_method': 'BLIK'
    }
    client.post(url, dct)
    assert Order.objects.all().first().user == normal_user
    assert Order.objects.all().first().address == 'Testowa 12'
    assert Order.objects.all().first().deliver_method == 'paczkomat'
    assert Order.objects.all().first().payment_method == 'BLIK'
    assert Order.objects.all().first().full_price == 1000
    assert OrderProducts.objects.all().first().amount == 1


@pytest.mark.django_db
def test_orders_no_user(client):
    url = reverse('orders')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_orders(client, normal_user, example_order, example_orderproduct):
    url = reverse('orders')
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['orders'][0] == example_order
    assert response.context['orders'][0].user == normal_user


@pytest.mark.django_db
def test_order_details_no_user(client, example_order):
    url = reverse('order', args=[example_order.id])
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_order_details_another_user(client, other_normal_user, example_order, example_orderproduct):
    url = reverse('order', args=[example_order.id])
    client.force_login(other_normal_user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_order_details(client, normal_user, example_order, example_orderproduct):
    url = reverse('order', args=[example_order.id])
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['order'] == example_order


@pytest.mark.django_db
def test_liked_products_no_user(client):
    url = reverse('liked_products')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_liked_products(client, normal_user, example_product, example_liked_products):
    url = reverse('liked_products')
    client.force_login(normal_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['products'][0] == example_product
    assert response.context['products'].count() == 1

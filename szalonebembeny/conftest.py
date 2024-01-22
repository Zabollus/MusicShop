import pytest
from django.contrib.auth.models import User, Permission

from szalonebembeny.models import Product, Category, Profile, Comment, Cart, CartProducts, Order, OrderProducts


@pytest.fixture
def six_products_two_categories():
    category1 = Category.objects.create(name='Instrumenty strunowe', description='Trzeba grać na strunach')
    category2 = Category.objects.create(name='Instrumenty dęte', description='Trzeba dmuchać')
    Product.objects.create(name='Gitara elektryczna', slug='gitara_elektryczna',
                           description='Gitara wymagająca wzmacniacza i prądu', category=category1,
                           price=1000, stock=10, votes=5, score=8.0)
    Product.objects.create(name='Trąbka', slug='trabka',
                           description='Można zagrać hejnał', category=category2,
                           price=1200, stock=30, votes=20, score=10.0)
    Product.objects.create(name='Gitara basowa', slug='gitara_basowa',
                           description='Gitara wymagająca wzmacniacza i prądu, sluży do ciężkich brzmień',
                           category=category1, price=1500, stock=50, votes=3, score=9.0)
    Product.objects.create(name='Gitara akustyczna', slug='gitara_akustyczna',
                           description='Gitara wyposażona w pudło rezonansowe', category=category1,
                           price=2000, stock=15, votes=8, score=6.0)
    Product.objects.create(name='Ukulele', slug='ukulele',
                           description='Mała gitarka', category=category1,
                           price=1800, stock=12, votes=10, score=7.5)
    Product.objects.create(name='Puzon', slug='puzon',
                           description='Instrument dety z grupy aerofonów ustnikowych', category=category2,
                           price=2600, stock=22, votes=0, score=-1)


@pytest.fixture
def user_worker():
    u = User.objects.create_user(username='worker', password='work')
    permission = Permission.objects.all().filter(content_type_id__in=[8, 10])
    u.user_permissions.set(permission)
    return u


@pytest.fixture
def normal_user():
    return User.objects.create_user(username='Test', password='1234', first_name='Jan',
                                    last_name='Kowalski', email='test@test.pl')


@pytest.fixture
def normal_user_profile(normal_user):
    return Profile.objects.create(user=normal_user, phone_number='123456789', address='Testowa 1')


@pytest.fixture
def normal_user_cart(normal_user):
    return Cart.objects.create(user=normal_user)


@pytest.fixture
def example_category():
    return Category.objects.create(name='test', description='opis testowy')


@pytest.fixture
def example_product(normal_user, example_category):
    return Product.objects.create(name='Gitara elektryczna', slug='gitara_elektryczna',
                                  description='Gitara wymagająca wzmacniacza i prądu', category=example_category,
                                  price=1000, stock=10, votes=5, score=8.0)


@pytest.fixture
def example_comment(example_product, normal_user):
    return Comment.objects.create(product=example_product, user=normal_user, content='Polecam', score=7.0)


@pytest.fixture
def example_cartproduct(example_product, normal_user_cart):
    return CartProducts.objects.create(cart=normal_user_cart, product=example_product, amount=1)


@pytest.fixture
def example_order(example_product, normal_user):
    return Order.objects.create(user=normal_user, address='Testowa 45', deliver_method='poczta',
                                payment_method='przelew', full_price=3000)


@pytest.fixture
def example_orderproduct(example_product, example_order):
    return OrderProducts.objects.create(order=example_order, product=example_product, amount=3)


@pytest.fixture
def other_normal_user():
    return User.objects.create_user(username='nick', password='54321', first_name='Piotr',
                                    last_name='Zieliński', email='test@test.com')


@pytest.fixture
def example_liked_products(normal_user, normal_user_profile, example_product):
    normal_user_profile.liked_products.add(example_product)

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
                           description='Gitara wymagająca wzmacniacza i prądu, sluży do ciężkich brzmień', category=category1,
                           price=1500, stock=50, votes=3, score=9.0)
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
    u = User.objects.create_user(username='Test', password='1234')
    return u


@pytest.fixture
def example_category():
    return Category.objects.create(name='test', description='opis testowy')


@pytest.fixture
def example_product():
    category1 = Category.objects.create(name='Instrumenty strunowe', description='Trzeba grać na strunach')
    return Product.objects.create(name='Gitara elektryczna', slug='gitara_elektryczna',
                           description='Gitara wymagająca wzmacniacza i prądu', category=category1,
                           price=1000, stock=10, votes=5, score=8.0)


@pytest.fixture
def example_comment():
    category1 = Category.objects.create(name='Instrumenty strunowe', description='Trzeba grać na strunach')
    product1 = Product.objects.create(name='Gitara elektryczna', slug='gitara_elektryczna',
                                  description='Gitara wymagająca wzmacniacza i prądu', category=category1,
                                  price=1000, stock=10, votes=5, score=8.0)
    u = User.objects.create_user(username='Test', password='1234')
    return Comment.objects.create(product=product1, user=u, content='Polecam', score=7.0)

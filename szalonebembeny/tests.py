from django.test import TestCase
from django.urls import reverse
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

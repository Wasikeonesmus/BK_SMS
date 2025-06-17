import pytest
from django.urls import reverse
from django.test import Client
from core.models import User, Sale, Product, Category
from decimal import Decimal

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_product():
    category = Category.objects.create(name='Test Category')
    return Product.objects.create(
        name='Test Product',
        price=Decimal('10.00'),
        category=category,
        stock_quantity=100
    )

def test_login_view(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert 'registration/login.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_dashboard_view_requires_login(client):
    response = client.get(reverse('dashboard'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_dashboard_view_with_login(client, admin_user):
    client.login(username='admin', password='testpass123')
    response = client.get(reverse('dashboard'))
    assert response.status_code == 200
    assert 'dashboard.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_pos_view_requires_login(client):
    response = client.get(reverse('pos'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_pos_view_with_login(client, admin_user):
    client.login(username='admin', password='testpass123')
    response = client.get(reverse('pos'))
    assert response.status_code == 200
    assert 'pos.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_inventory_view_requires_login(client):
    response = client.get(reverse('inventory'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_inventory_view_with_login(client, admin_user):
    client.login(username='admin', password='testpass123')
    response = client.get(reverse('inventory'))
    assert response.status_code == 200
    assert 'inventory.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_reports_view_requires_login(client):
    response = client.get(reverse('reports'))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_reports_view_with_login(client, admin_user):
    client.login(username='admin', password='testpass123')
    response = client.get(reverse('reports'))
    assert response.status_code == 200
    assert 'reports.html' in [t.name for t in response.templates] 
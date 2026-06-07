import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def registered_user(db):
    return User.objects.create_user(
        email='nik@test.com',
        username='nik',
        password='test1234'
    )


@pytest.fixture
def auth_client(client, registered_user):
    res = client.post(reverse('login'), {
        'email': 'nik@test.com',
        'password': 'test1234'
    }, format='json')
    token = res.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


# --- Register tests ---

@pytest.mark.django_db
def test_register_valid_data(client):
    res = client.post(reverse('register'), {
        'email': 'newuser@test.com',
        'username': 'newuser',
        'password': 'pass1234'
    }, format='json')
    assert res.status_code == 201
    assert 'tokens' in res.data
    assert res.data['user']['email'] == 'newuser@test.com'


@pytest.mark.django_db
def test_register_duplicate_email(client, registered_user):
    res = client.post(reverse('register'), {
        'email': 'nik@test.com',
        'username': 'another',
        'password': 'pass1234'
    }, format='json')
    assert res.status_code == 400


@pytest.mark.django_db
def test_register_missing_password(client):
    res = client.post(reverse('register'), {
        'email': 'someone@test.com',
        'username': 'someone'
    }, format='json')
    assert res.status_code == 400


# --- Login tests ---

@pytest.mark.django_db
def test_login_valid_credentials(client, registered_user):
    res = client.post(reverse('login'), {
        'email': 'nik@test.com',
        'password': 'test1234'
    }, format='json')
    assert res.status_code == 200
    assert 'access' in res.data
    assert 'refresh' in res.data


@pytest.mark.django_db
def test_login_wrong_password(client, registered_user):
    res = client.post(reverse('login'), {
        'email': 'nik@test.com',
        'password': 'wrongpass'
    }, format='json')
    assert res.status_code == 401


# --- Profile tests ---

@pytest.mark.django_db
def test_profile_authenticated(auth_client, registered_user):
    res = auth_client.get(reverse('profile'))
    assert res.status_code == 200
    assert res.data['email'] == 'nik@test.com'


@pytest.mark.django_db
def test_profile_unauthenticated(client):
    res = client.get(reverse('profile'))
    assert res.status_code == 401
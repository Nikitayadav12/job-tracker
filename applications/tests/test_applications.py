import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from applications.models import JobApplication

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='nik@test.com',
        username='nik',
        password='test1234'
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        email='other@test.com',
        username='other',
        password='test1234'
    )


@pytest.fixture
def auth_client(client, user):
    res = client.post(reverse('login'), {
        'email': 'nik@test.com',
        'password': 'test1234'
    }, format='json')
    token = res.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def sample_application(db, user):
    return JobApplication.objects.create(
        user=user,
        company_name='Google',
        role_title='Python Developer',
        status='Applied',
        location='Pune',
    )


# --- CRUD tests ---

@pytest.mark.django_db
def test_create_application(auth_client):
    res = auth_client.post('/api/applications/', {
        'company_name': 'Amazon',
        'role_title': 'Backend Developer',
        'status': 'Applied',
        'location': 'Remote',
    }, format='json')
    assert res.status_code == 201
    assert res.data['company_name'] == 'Amazon'


@pytest.mark.django_db
def test_list_applications_only_own(auth_client, sample_application, other_user):
    # Create application for other user
    JobApplication.objects.create(
        user=other_user,
        company_name='Microsoft',
        role_title='SDE',
        status='Applied',
    )
    res = auth_client.get('/api/applications/')
    assert res.status_code == 200
    # Should only see own application, not other user's
    assert len(res.data) == 1
    assert res.data[0]['company_name'] == 'Google'


@pytest.mark.django_db
def test_update_status(auth_client, sample_application):
    res = auth_client.patch(
        f'/api/applications/{sample_application.id}/',
        {'status': 'Interview'},
        format='json'
    )
    assert res.status_code == 200
    assert res.data['status'] == 'Interview'


@pytest.mark.django_db
def test_delete_application(auth_client, sample_application):
    res = auth_client.delete(f'/api/applications/{sample_application.id}/')
    assert res.status_code == 204
    assert JobApplication.objects.count() == 0


@pytest.mark.django_db
def test_unauthenticated_cannot_access(client):
    res = client.get('/api/applications/')
    assert res.status_code == 401


# --- Filter tests ---

@pytest.mark.django_db
def test_filter_by_status(auth_client, user):
    JobApplication.objects.create(user=user, company_name='A', role_title='Dev', status='Applied')
    JobApplication.objects.create(user=user, company_name='B', role_title='Dev', status='Interview')
    res = auth_client.get('/api/applications/?status=Interview')
    assert all(a['status'] == 'Interview' for a in res.data)

# --- Notes tests ---

@pytest.mark.django_db
def test_add_note_to_application(auth_client, sample_application):
    res = auth_client.post(
        f'/api/applications/{sample_application.id}/notes/',
        {'content': 'Called HR today.'},
        format='json'
    )
    assert res.status_code == 201
    assert res.data['content'] == 'Called HR today.'


@pytest.mark.django_db
def test_dashboard_summary(auth_client, user):
    JobApplication.objects.create(user=user, company_name='A', role_title='Dev', status='Applied')
    JobApplication.objects.create(user=user, company_name='B', role_title='Dev', status='Rejected')
    res = auth_client.get('/api/dashboard/summary/')
    assert res.status_code == 200
    assert res.data['total'] == 2
    assert res.data['by_status']['Applied'] == 1
    assert res.data['by_status']['Rejected'] == 1
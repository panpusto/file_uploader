import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestClassAccounts:
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            email='test_user@email.com',
            password='testpass123'
        )
        assert get_user_model().objects.count() == 1
        assert user.email == 'test_user@email.com'

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            email='superuser@email.com',
            password='testpass123'
        )
        assert get_user_model().objects.count() == 1
        assert superuser.email == 'superuser@email.com'
        assert superuser.is_staff == 1
        assert superuser.is_superuser == 1
        assert superuser.is_active == 1


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.mark.django_db
class TestClassJSONWebToken:
    def test_token_obtain_pair_view_with_get(self, client):
        get_response = client.get(reverse('token_obtain_pair'))
        assert get_response.status_code == 405

    def test_token_obtain_pair_view_with_post_for_register_user(self, client):
        get_user_model().objects.create_user(
            email='test_user@email.com',
            password='testpass123'
        )
        post_response = client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'test_user@email.com',
                'password': 'testpass123'
            })
        assert post_response.status_code == 200
    
    def test_token_obtain_pair_view_with_post_for_non_register_user(self, client):
        post_response = client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'fake_user@email.com',
                'password': 'testpass123'
            })
        assert post_response.status_code == 401

    def test_token_refresh_with_get(self, client):
        get_response = client.get(reverse('token_refresh'))
        assert get_response.status_code == 405
    
    def test_token_refresh_with_post_for_correct_token(self, client):
        get_user_model().objects.create_user(
            email='test_user@email.com',
            password='testpass123'
        )
        generate_token = client.post(
            reverse('token_obtain_pair'),
            {
                'email': 'test_user@email.com',
                'password': 'testpass123'
            })
        refresh_token = generate_token.json()['refresh']
        post_response = client.post(
            reverse('token_refresh'),
            {
                'refresh': refresh_token
            }
        )
        assert post_response.status_code == 200

    def test_token_refresh_with_post_for_fake_token(self, client):
        post_response = client.post(
            reverse('token_refresh'),
            {
                'refresh': 'some424_)fake_##_token65540'
            }
        )
        assert post_response.status_code == 401
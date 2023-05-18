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


@pytest.mark.django_db
class TestClassRegisterView:
    def test_register_api_view_with_get(self, client):
        get_response = client.get(reverse('register_user'))
        assert get_response.status_code == 405

    def test_register_api_view_with_post_correct_inputs(self, client):
        post_response = client.post(
            reverse('register_user'),
            {
                'email': 'test_user1@email.com',
                'password': 'Testpass123!',
                'password2': 'Testpass123!'
            }
        )
        assert post_response.status_code == 201
        assert post_response.json()['email'] == 'test_user1@email.com'
    
    def test_register_api_view_with_post_not_correct_email(self, client):
        post_response = client.post(
            reverse('register_user'),
            {
                'email': 'wrong_email.com',
                'password': 'Testpass123!',
                'password2': 'Testpass123!'
            }
        )
        assert post_response.status_code == 400

    def test_register_api_view_with_post_not_unique_email(self, client):
        get_user_model().objects.create_user(
            email='test_user@email.com',
            password='testpass123'
        )
        post_response = client.post(
            reverse('register_user'),
            {
                'email': 'test_user@email.com',
                'password': 'Testpass123!',
                'password2': 'Testpass123!'
            }
        )
        assert post_response.status_code == 400
        assert post_response.json()['email'] == ['Account with this email address already exists.']

    def test_register_api_view_with_post_not_matched_passwords(self, client):
        post_response = client.post(
            reverse('register_user'),
            {
                'email': 'testuser@email.com',
                'password': 'Testpass123!',
                'password2': 'testpassword666'
            }
        )
        assert post_response.status_code == 400
    
    def test_register_api_view_with_post_too_short_password(self, client):
        post_response = client.post(
            reverse('register_user'),
            {
                'email': 'testuser@email.com',
                'password': 'te!1W',
                'password2': 'te!1W'
            }
        )
        assert post_response.status_code == 400
        assert post_response.json()['password'] == ['This password is too short. It must contain at least 8 characters.']

    def test_register_api_view_with_post_password_without_digit(self, client):
        post_response = client.post(
            reverse('register_user'),
            {
                'email': 'testuser@email.com',
                'password': 'Testpass!',
                'password2': 'Testpass!'
            }
        )
        assert post_response.status_code == 400
        assert post_response.json()['password'] == ['This password must contain any digit.']

    def test_register_api_view_with_post_password_without_punctuation(self, client):
        post_response = client.post(
            reverse('register_user'),
            {
                'email': 'testuser@email.com',
                'password': 'Testpass123',
                'password2': 'Testpass123'
            }
        )
        assert post_response.status_code == 400
        assert post_response.json()['password'] == ['This password must contain any punctuation sign.']
    
    def test_register_api_view_with_post_password_without_uppercase(self, client):
        post_response = client.post(
            reverse('register_user'),
            {
                'email': 'testuser@email.com',
                'password': 'testpass123!',
                'password2': 'testpass123!'
            }
        )
        assert post_response.status_code == 400
        assert post_response.json()['password'] == ['This password must contain any uppercase.']
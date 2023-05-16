import pytest
from django.contrib.auth import get_user_model


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

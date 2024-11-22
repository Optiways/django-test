import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def create_admin_user():
    user_model = get_user_model()
    admin_user = user_model.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword'
    )
    return admin_user

@pytest.fixture
def authenticated_client(create_admin_user, client):
    client.login(username='admin', password='adminpassword')
    return client

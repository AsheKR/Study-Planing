from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from rest_framework.authtoken.models import Token

User = get_user_model()


class TestUserAPI:

    def test_create_member_api(self, client):
        context = {
            'user_id': 'example',
            'password': 'asd',
            'email': 'ex@ex.com',
        }
        response = client.post(resolve_url('api:users:user_create'), context)

        assert response.status_code == 201
        assert response.json()['token'] == Token.objects.get(user=User.objects.first()).key

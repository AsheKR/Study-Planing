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

    def test_error_occurs_when_duplication_the_id_or_email(self, client):
        context = {
            'user_id': 'example',
            'password': 'asd',
            'email': 'ex@ex.com',
        }
        client.post(resolve_url('api:users:user_create'), context)
        context['email'] = 'ex2@ex.com'
        response = client.post(resolve_url('api:users:user_create'), context)

        assert response.status_code == 400, 'id가 중복되어 생성되면 안된다.'
        assert response.data.get('user_id')

        context['email'] = 'ex@ex.com'
        context['user_id'] = 'differentID'
        response = client.post(resolve_url('api:users:user_create'), context)

        assert response.status_code == 400, 'email이 중복되어 생성되면 안된다.'
        assert response.data.get('email')

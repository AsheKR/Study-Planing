from django.shortcuts import resolve_url


class TestRepositoryAPI:

    def _create_stub_members(self, client):
        context = {
            'user_id': 'example',
            'password': 'asd',
            'email': 'ex@ex.com',
        }
        response = client.post(resolve_url('api:users:user_create'), context)
        return response

    def _create_stub_repository(self, client):
        token = self._create_stub_members(client).json()['token']
        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'name': 'my-repo'
        }

        response = client.post(resolve_url('api:repository:repository_create'), data=context, **header)
        return response, token

    def test_create_repository_api(self, client):
        response, _ = self._create_stub_repository(client)

        assert response.status_code == 201

    def test_cannot_create_repository_with_same_name(self, client):
        _, token = self._create_stub_repository(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'name': 'my-repo'
        }

        response = client.post(resolve_url('api:repository:repository_create'), data=context, **header)

        assert response.status_code == 400

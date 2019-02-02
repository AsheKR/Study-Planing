import pytest
from django.shortcuts import resolve_url

from repository.models import Repository


class TestStubMethodMixin:

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

        response = client.post(resolve_url('api:repository:repository_list_create'), data=context, **header)
        return response, token


class TestRepositoryAPI(TestStubMethodMixin):

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

        response = client.post(resolve_url('api:repository:repository_list_create'), data=context, **header)

        assert response.status_code == 400

    def test_list_repository_api(self, client):
        _, token = self._create_stub_repository(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }
        context = {
            'name': 'my-repo2'
        }
        client.post(resolve_url('api:repository:repository_list_create'), data=context, **header)

        response = client.get(resolve_url('api:repository:repository_list_create'))

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_retrieve_repository_api(self, client):
        _, token = self._create_stub_repository(client)

        pk = Repository.objects.first().pk

        response = client.get(resolve_url('api:repository:repository_retrieve_update_destroy', pk=pk))

        assert response.status_code == 200

        assert response.json().get('name')
        assert response.json().get('owner')
        assert response.json().get('root_folder')

    def test_patch_repository_api(self, client):
        _, token = self._create_stub_repository(client)

        pk = Repository.objects.first().pk

        change_name = 'change_dir_name'
        context = {
            'name': change_name
        }
        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        response = client.patch(resolve_url('api:repository:repository_retrieve_update_destroy', pk=pk),
                                data=context,
                                **header,
                                content_type='application/json')

        assert response.status_code == 200

        assert Repository.objects.first().name == change_name

    def test_cannot_patch_repository_with_same_name(self, client):
        _, token = self._create_stub_repository(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }
        context = {
            'name': 'my-repo2'
        }
        client.post(resolve_url('api:repository:repository_list_create'), data=context, **header)

        client.get(resolve_url('api:repository:repository_list_create'))

        response = client.patch(resolve_url('api:repository:repository_retrieve_update_destroy', pk=1),
                                data=context,
                                **header,
                                content_type='application/json')

        assert response.status_code == 400

    def test_destroy_repository_api(self, client):
        _, token = self._create_stub_repository(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        response = client.delete(resolve_url('api:repository:repository_retrieve_update_destroy', pk=1),
                                 **header,
                                 content_type='application/json')

        assert response.status_code == 204

import pytest
from django.core.files.base import ContentFile
from django.shortcuts import resolve_url

from repository.tests.stub_mixin import TestStubMethodMixin


class TestManagedFileAPI(TestStubMethodMixin):

    def test_create_managed_file_api(self, client):
        response, token = self._create_stub_managed_file(client)

        assert response.status_code == 201

    def test_create_folder_with_managed_file_api(self, client):
        response, _ = self._create_stub_folder_with_managed_file(client)

        assert response.status_code == 201

    def test_create_nested_file_with_managed_file_api(self, client):
        response, token = self._create_stub_folder_with_managed_file(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'name': 'managed_file',
            'file': ContentFile('Hello World!'),
        }

        response = client.post(resolve_url('api:repository:managed_file_create', repository_pk=1, dir_pk=2), data=context, **header)

        assert response.status_code == 201

    def test_cannot_create_same_name_in_same_directory(self, client):
        response, token = self._create_stub_managed_file(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'name': 'managed_file',
            'file': ContentFile('Hello World!'),
        }

        response = client.post(resolve_url('api:repository:managed_file_create', repository_pk=1, dir_pk=1), data=context, **header)

        assert response.status_code == 400

    def test_retrieve_managed_file_api(self, client):
        response, _ = self._create_stub_managed_file(client)

        response = client.get(resolve_url('api:repository:managed_file_retrieve_update_destroy', repository_pk=1, dir_pk=1, pk=2))

        assert response.status_code == 200
        assert response.json()['name'] == 'managed_file'

    def test_patch_managed_file_api(self, client):
        response, token = self._create_stub_managed_file(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'name': 'change_file_name',
        }

        response = client.patch(
            resolve_url('api:repository:managed_file_retrieve_update_destroy',
                        repository_pk=1,
                        dir_pk=1,
                        pk=2),
            data=context, **header,
            content_type='application/json'
        )

        assert response.status_code == 200

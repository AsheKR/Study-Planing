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

    @pytest.mark.smoke
    def test_create_nested_file_with_managed_file_api(self, client):
        response, token = self._create_stub_folder_with_managed_file(client)

        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'repository': '1',
            'dir': '2',
            'name': 'managed_file',
            'file': ContentFile('Hello World!'),
        }

        response = client.post(resolve_url('api:repository:managed_file_list_create'), data=context, **header)

        assert response.status_code == 201

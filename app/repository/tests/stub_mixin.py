from django.core.files.base import ContentFile
from django.shortcuts import resolve_url


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

    def _create_stub_managed_file(self, client):
        _, token = self._create_stub_repository(client)
        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'repository': '1',
            'dir': '1',
            'name': 'managed_file',
            'file': ContentFile('Hello World!'),
        }

        response = client.post(resolve_url('api:repository:managed_file_list_create'), data=context, **header)

        return response, token

    def _create_stub_folder_with_managed_file(self, client):
        _, token = self._create_stub_repository(client)
        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'repository': '1',
            'dir': '1',
            'name': 'managed_folder',
        }

        response = client.post(resolve_url('api:repository:managed_file_list_create'), data=context, **header)

        return response, token

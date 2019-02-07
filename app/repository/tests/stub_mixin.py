import shutil

from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import resolve_url


class TestStubMethodMixin:

    def teardown_method(self, method):
        shutil.rmtree(settings.MEDIA_ROOT)

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

        response = client.post(
            resolve_url(
                'api:repository:repository_list_create'),
            data=context,
            **header)
        return response, token

    def _create_stub_managed_file(self, client):
        _, token = self._create_stub_repository(client)
        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'name': 'managed_file',
            'file': ContentFile('Hello World!'),
        }

        response = client.post(
            resolve_url(
                'api:repository:managed_file_create', repository_pk=1, dir_pk=1),
            data=context,
            **header)

        return response, token

    def _create_stub_folder_with_managed_file(self, client):
        _, token = self._create_stub_repository(client)
        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'name': 'managed_folder',
        }

        response = client.post(
            resolve_url(
                'api:repository:managed_file_create', repository_pk=1, dir_pk=1),
            data=context,
            **header)

        return response, token

    def _create_stub_commit_with_file(self, client):
        _, token = self._create_stub_managed_file(client)
        header = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

        context = {
            'file': ContentFile('Nice To Meet You!'),
            'title': 'Hello to Nice',
        }

        response = client.post(
            resolve_url(
                'api:repository:commit_list_create',
                repository_pk=1,
                tracked_file_pk=1),
            data=context,
            **header)

        return response, token

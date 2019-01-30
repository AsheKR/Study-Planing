import random

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import IntegrityError

from repository.models import Repository, ManagedFile

User = get_user_model()


class TestRepositoryModel:

    def test_cannot_create_repository_by_none_user(self):
        with pytest.raises(IntegrityError):
            Repository.objects.create(
                name='First_Repo',
            )

    def test_cannot_create_repository_by_same_user_using_same_repo_name(self):
        user = User.objects.create_user(
            user_id='example1',
            password='123',
            email='a@a.com'
        )

        with pytest.raises(IntegrityError):
            Repository.objects.create(
                name='same_name',
                owner=user
            )
            Repository.objects.create(
                name='same_name',
                owner=user
            )

    def test_get_repository_dir_has_correct_path(self):
        user = User.objects.create_user(
            user_id='example1',
            password='123',
            email='a@a.com'
        )

        repo = Repository.objects.create(
            name='repo',
            owner=user
        )

        assert 'example1/repo' in repo.get_repository_dir


class TestManagedFileModel:
    def _create_stub_user_and_repository(self):
        self.user = User.objects.create_user(
            user_id='user',
            password='123',
            email='a@a.com'
        )
        self.repo = Repository.objects.create(
            name='repo',
            owner=self.user
        )

    def test_file_field_has_correct_path(self):
        self._create_stub_user_and_repository()
        myfile = ContentFile(random.choice('abcde'))
        obj = ManagedFile(
            repository=self.repo,
        )
        obj.file.save('file_name', myfile)
        assert '/user/repo/file_name' in obj.file.path

import hashlib
import os
import random

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import IntegrityError, models

from repository.models import Repository, ManagedFile, TrackedFileInfo

User = get_user_model()


class TestRepositoryModel:

    def test_cannot_create_repository_by_none_user(self):
        with pytest.raises(models.ObjectDoesNotExist):
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
                name='same_repo_name',
                owner=user
            )
            Repository.objects.create(
                name='same_repo_name',
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

    def test_create_repository_also_create_vcs_dir(self):
        user = User.objects.create_user(
            user_id='example1',
            password='123',
            email='a@a.com'
        )

        repo = Repository.objects.create(
            name='repo',
            owner=user
        )

        assert os.path.isdir(os.path.join(repo.get_repository_dir, '.vcs')) is True

    def test_create_repository_also_create_root_managed_folder(self):
        user = User.objects.create_user(
            user_id='example1',
            password='123',
            email='a@a.com'
        )

        repo = Repository.objects.create(
            name='repo',
            owner=user
        )

        assert repo.root_folder == ManagedFile.objects.first()


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

    def _create_managed_file(self, file_name, directory):
        my_file = ContentFile(random.choice('abcde'))
        self.managed_file = ManagedFile(
            create_author=self.user,
            name=file_name,
            dir=directory,
        )
        self.managed_file.file.save('file_name', my_file)

    def _create_managed_folder(self, folder_name, directory):
        self.managed_folder = ManagedFile.objects.create(
            create_author=self.user,
            name=folder_name,
            dir=directory,
        )

    def test_file_field_has_correct_path(self):
        self._create_stub_user_and_repository()
        self._create_managed_file('file_name', self.repo.root_folder)
        assert '/user/repo/file_name' in self.managed_file.file.path

    def test_create_file_also_create_a_commit(self):
        self._create_stub_user_and_repository()
        self._create_managed_file('file_name', self.repo.root_folder)
        assert TrackedFileInfo.objects.count() == 1

    def test_dir_has_full_dir_path(self):
        self._create_stub_user_and_repository()
        self._create_managed_folder('child_folder', self.repo.root_folder)

        assert self.managed_folder.get_parent_dir(self.managed_folder) + self.managed_folder.name == '/child_folder'

    def test_get_root_dir_object(self):
        self._create_stub_user_and_repository()
        self._create_managed_folder('child_folder', self.repo.root_folder)
        self._create_managed_file('file_name', self.repo.root_folder)

        assert self.managed_file.get_root_dir(self.managed_file) == self.repo.root_folder
        assert self.managed_folder.get_root_dir(self.managed_folder) == self.repo.root_folder

    def test_has_a_hash_value_for_the_file_name(self):
        self._create_stub_user_and_repository()
        self._create_managed_file('file_name', self.repo.root_folder)
        assert self.managed_file.file_hash == hashlib.sha1(str.encode('/file_name')).hexdigest()

    def test_recursive_directory_file_has_correct_parent_dir(self):
        self._create_stub_user_and_repository()
        self._create_managed_folder('first_folder', self.repo.root_folder)
        self._create_managed_folder('second_folder', self.managed_folder)
        self._create_managed_file('file_name', self.managed_folder)
        assert '/user/repo/first_folder/second_folder/file_name' in self.managed_file.file.path

    def test_managed_file_also_create_commit_message_with_commit_hash(self):
        self._create_stub_user_and_repository()
        self._create_managed_file('file_name', self.repo.root_folder)
        assert self.managed_file.trackedfileinfo.commit_set.count() == 1
        assert self.managed_file.trackedfileinfo.commit_set.first().commit_hash


class TestTrackedFileInfoModel:

    def _create_stub_user_and_repository_and_file(self):
        self.user = User.objects.create_user(
            user_id='user',
            password='123',
            email='a@a.com'
        )
        self.repo = Repository.objects.create(
            name='repo',
            owner=self.user
        )
        file = ContentFile(random.choice('abcde'))
        self.file = ManagedFile(
            name='file_name',
            dir=self.repo.root_folder,
        )
        self.file.file.save('file_name', file)

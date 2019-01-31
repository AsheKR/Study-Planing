import hashlib
import os
import random

import pytest
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import IntegrityError

from repository.models import Repository, ManagedFile, TrackedFileInfo

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

    def test_file_field_has_correct_path(self):
        self._create_stub_user_and_repository()
        myfile = ContentFile(random.choice('abcde'))
        obj = ManagedFile(
            name='file_name',
            dir=self.repo.root_folder,
        )
        obj.file.save('file_name', myfile)
        assert '/user/repo/file_name' in obj.file.path

    def test_create_file_also_create_a_commit(self):
        self._create_stub_user_and_repository()
        myfile = ContentFile(random.choice('abcde'))
        obj = ManagedFile(
            name='file_name',
            dir = self.repo.root_folder,
        )
        obj.file.save('file_name', myfile)
        assert TrackedFileInfo.objects.count() == 1

    def test_dir_has_full_dir_path(self):
        self._create_stub_user_and_repository()
        myfolder = ManagedFile.objects.create(
            name='child_folder',
            dir=self.repo.root_folder
        )

        assert myfolder.get_parent_dir(myfolder.dir) + myfolder.name == '/child_folder'

    def test_has_a_hash_value_for_the_file_name(self):
        self._create_stub_user_and_repository()
        myfile = ContentFile(random.choice('abcde'))
        obj = ManagedFile(
            name='file_name',
            dir=self.repo.root_folder,
        )
        obj.file.save('file_name', myfile)
        assert obj.file_hash == hashlib.sha1(str.encode('/file_name')).hexdigest()

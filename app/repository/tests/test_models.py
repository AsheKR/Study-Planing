import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from repository.models import Repository

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

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

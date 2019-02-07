import pytest

from repository.models import Commit
from repository.tests.stub_mixin import TestStubMethodMixin


class TestCommitAPI(TestStubMethodMixin):

    @pytest.mark.smoke
    def test_create_commit_api(self, client):
        response, _ = self._create_stub_commit_with_file(client)

        assert response.status_code == 201
        assert Commit.objects.last().title == 'Hello to Nice'

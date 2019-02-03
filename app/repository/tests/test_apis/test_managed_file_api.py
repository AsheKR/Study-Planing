from repository.tests.stub_mixin import TestStubMethodMixin


class TestManagedFileAPI(TestStubMethodMixin):

    def test_create_managed_file_api(self, client):
        response, token = self._create_stub_managed_file(client)

        assert response.status_code == 201

    def test_create_folder_with_managed_file_api(self, client):
        response, _ = self._create_stub_folder_with_managed_file(client)

        assert response.status_code == 201

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserModel:

    def test_fields_that_must_be_filled_in_when_creating_user(self):
        user_info = (('user_id', 'example1'), ('password', 'asd'), ('email', 'a@a.com'), )
        test_fields = dict()

        for field_name, field_value in user_info:
            with pytest.raises(TypeError) as e:
                User.objects.create_user(
                    **test_fields,
                )
            test_fields[field_name] = field_value

        user = User.objects.create_user(
            **test_fields
        )

        assert user == User.objects.first(), 'User Create Failed'

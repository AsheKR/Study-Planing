import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

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

    def test_user_id_must_be_unique(self):
        first_user_info = (('user_id', 'same_user_id'), ('password', 'asd'), ('email', 'a@a.com'),)
        second_user_info = (('user_id', 'same_user_id'), ('password', 'asd'), ('email', 'b@b.com'),)

        with pytest.raises(IntegrityError):
            User.objects.create_user(
                **dict(first_user_info),
            )

            User.objects.create_user(
                **dict(second_user_info),
            )

    def test_user_email_must_be_uinque(self):
        first_user_info = (('user_id', 'id1'), ('password', 'asd'), ('email', 'same@same.com'),)
        second_user_info = (('user_id', 'id2'), ('password', 'asd'), ('email', 'same@same.com'),)

        with pytest.raises(IntegrityError):
            User.objects.create_user(
                **dict(first_user_info),
            )

            User.objects.create_user(
                **dict(second_user_info),
            )
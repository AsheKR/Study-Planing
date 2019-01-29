import pytest


class TestMemberModel:

    def test_fields_that_must_be_filled_in_when_creating_user(self):
        user_info = (('user_id', 'example1'), ('password', 'asd'), ('email', 'a@a.com'), )
        test_fields = dict()

        for field_name, field_value in user_info:
            User.objects.create_user(
                **test_fields,
            )
            test_fields[field_name] = field_value

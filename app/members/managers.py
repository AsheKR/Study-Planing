from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_id, email, password, **extra_fields):
        if not user_id:
            raise ValueError('The given User ID must be set')
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(user_id=user_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_id, email, password, **extra_fields)

    def create_superuser(self, user_id, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_id, email, password, **extra_fields)

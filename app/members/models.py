from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from members.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField('유저아이디', max_length=15, unique=True, )
    email = models.EmailField('유저이메일', unique=True, )

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = ('유저', )
        verbose_name_plural = ('유저', )

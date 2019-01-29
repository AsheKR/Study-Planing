from django.conf import settings
from django.db import models


class Repository(models.Model):
    name = models.CharField(
        max_length=50,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            'name',
            'owner',
        )

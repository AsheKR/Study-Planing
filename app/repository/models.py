import os

from django.conf import settings
from django.db import models

from repository.filesystems import upload_dynamic_path, ManagedFileSystemStorage


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

    @property
    def get_repository_dir(self):
        return os.path.join(settings.ROOT_DIR, '.media', self.owner.user_id, self.name)


class ManagedFile(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        upload_to=upload_dynamic_path,
        storage=ManagedFileSystemStorage()
    )

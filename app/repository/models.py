import os
import pathlib

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

    def save(self, *args, **kwargs):
        super().save()
        pathlib.Path(os.path.join(self.get_repository_dir, '.vcs')).mkdir(parents=True, exist_ok=True)


class ManagedFile(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        upload_to=upload_dynamic_path,
        storage=ManagedFileSystemStorage()
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        TrackedFileInfo.objects.create(
            managed_file=self,
        )


class TrackedFileInfo(models.Model):
    managed_file = models.ForeignKey(
        ManagedFile,
        on_delete=models.CASCADE,
    )

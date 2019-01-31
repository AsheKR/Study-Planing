import hashlib
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
    root_folder = models.OneToOneField(
        'ManagedFile',
        on_delete=models.CASCADE,
        related_name='root_repository',
        related_query_name='root_repository',
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
        root_folder = ManagedFile.objects.create(
            name='/',
        )
        self.root_folder = root_folder
        super().save()
        pathlib.Path(os.path.join(self.get_repository_dir, '.vcs')).mkdir(parents=True, exist_ok=True)


class ManagedFile(models.Model):
    name = models.CharField(
        max_length=20,
    )
    file_hash = models.CharField(
        max_length=40,
    )
    file = models.FileField(
        upload_to=upload_dynamic_path,
        storage=ManagedFileSystemStorage(),
        blank=True,
        null=True,
    )
    dir = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __repr__(self):
        return self.name

    def get_root_dir(self, parent_dir):
        if not parent_dir.dir:
            return parent_dir

        return self.get_root_dir(parent_dir.dir)

    def get_parent_dir(self, parent_dir):
        if not parent_dir.dir:
            return ''

        return parent_dir.dir.name + self.get_parent_dir(parent_dir.dir)

    def save(self, *args, **kwargs):
        dir_full_path = self.get_parent_dir(self) + self.name
        file_hash = hashlib.sha1(str.encode(dir_full_path)).hexdigest()

        self.file_hash = file_hash

        super().save(*args, **kwargs)

        if self.file:
            TrackedFileInfo.objects.create(
                managed_file=self,
            )


class TrackedFileInfo(models.Model):
    managed_file = models.ForeignKey(
        ManagedFile,
        on_delete=models.CASCADE,
    )

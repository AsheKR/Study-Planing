import hashlib
import os
import pathlib

from django.conf import settings
from django.db import models
from django.utils import timezone

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
            create_author=self.owner,
        )
        self.root_folder = root_folder
        super().save()
        pathlib.Path(os.path.join(self.get_repository_dir, '.vcs')).mkdir(parents=True, exist_ok=True)


class ManagedFile(models.Model):
    create_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
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

        if parent_dir.dir.name == '/':
            name = ''
        else:
            name = parent_dir.dir.name

        return self.get_parent_dir(parent_dir.dir) + '/' + name

    def save(self, *args, **kwargs):
        dir_full_path = self.get_parent_dir(self) + self.name
        file_hash = hashlib.sha1(str.encode(dir_full_path)).hexdigest()

        self.file_hash = file_hash

        super().save(*args, **kwargs)

        if self.file:
            track = TrackedFileInfo.objects.create(
                managed_file=self,
            )
            Commit.objects.create(
                tracked_file=track,
                author=self.create_author,
                title=self.name+'생성됨.',
            )


class TrackedFileInfo(models.Model):
    managed_file = models.OneToOneField(
        ManagedFile,
        on_delete=models.CASCADE,
    )
    # head는 file_content_hash 내용을 가진다.
    head = models.CharField(
        max_length=40,
    )


class Commit(models.Model):
    tracked_file = models.ForeignKey(
        TrackedFileInfo,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=50,
    )
    content = models.TextField(
        blank=True,
        null=True,
    )
    commit_hash = models.CharField(
        max_length=40,
    )
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        now = timezone.now()
        full_str = self.tracked_file.managed_file.name + str(now)
        self.commit_hash = hashlib.sha1(str.encode(full_str)).hexdigest()
        self.created_at = now
        super().save(*args, **kwargs)

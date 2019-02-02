import hashlib
import os
import pathlib

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone

from repository.filesystems import upload_dynamic_path, ManagedFileSystemStorage
from repository.vcs_mixin import VCSMixin


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
        """
        Repository의 Root Directory의 문자열을 리턴하는 프로퍼티
        """
        return os.path.join(settings.ROOT_DIR, '.media', self.owner.user_id, self.name)

    def save(self, *args, **kwargs):
        root_folder = ManagedFile.objects.create(
            name='/',
            create_author=self.owner,
        )
        self.root_folder = root_folder
        super().save()
        destination = os.path.join(self.get_repository_dir, '.vcs', 'patch')
        pathlib.Path(destination).mkdir(parents=True, exist_ok=True)


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
        """
        해당 레포지토리의 Root ('/') 의 ManagedFile Object를 가져오는 함수
        """
        if not parent_dir.dir:
            return parent_dir

        return self.get_root_dir(parent_dir.dir)

    def get_parent_dir(self, parent_dir):
        """
        해당 레포지토리의 루트로부터 현재 파일 혹은 폴더의 부모 폴더까지의 경로를 가져오는 함수
        """
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
            new_file = ContentFile('')
            Commit.commit(
                new_file=new_file,
                tracked_file=track,
                author=self.create_author,
                title=self.name + '생성됨.',
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


class Commit(models.Model, VCSMixin):
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
        now = self.created_at if self.created_at else timezone.now()
        self.created_at = now
        self.commit_hash = Commit.calc_commit_hash(self.tracked_file, now)
        super().save(*args, **kwargs)

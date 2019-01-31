import os

from django.core.files.storage import FileSystemStorage


def upload_dynamic_path(instance, filename):
    root_dir = instance.get_root_dir(instance)
    repository = root_dir.root_repository

    return '{0}/{1}/{2}'.format(
        repository.owner,
        repository.name,
        filename,
    )


class ManagedFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name

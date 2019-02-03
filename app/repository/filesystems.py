import os

from django.core.files.storage import FileSystemStorage


def upload_dynamic_path(instance, filename):
    root_dir = instance.get_root_dir(instance)
    parent_dir = instance.get_parent_dir(instance)
    repository = root_dir.root_repository

    value = '{0}/{1}/{2}/{3}'.format(
        repository.owner,
        repository.name,
        parent_dir,
        instance.name,
    )

    return value


class ManagedFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name

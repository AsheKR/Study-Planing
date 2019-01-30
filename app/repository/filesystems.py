import os

from django.core.files.storage import FileSystemStorage


def upload_dynamic_path(instance, filename):
    return '{0}/{1}/{2}'.format(
        instance.repository.owner,
        instance.repository.name,
        filename,
    )


class ManagedFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name

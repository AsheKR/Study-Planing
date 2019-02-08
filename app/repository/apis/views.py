import os
import shutil

from rest_framework import generics, serializers, status
from rest_framework.response import Response

from repository.apis.permissions import RepositoryPermissions
from repository.apis.serializers import RepositorySerializer, ManagedFileSerializer, CommitSerializer
from repository.models import Repository, ManagedFile, Commit


class RepositoryListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer


class RepositoryRetrieveUpdateDestroyGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = (
        RepositoryPermissions,
    )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        repo = Repository.objects.filter(pk=instance.pk)

        source = repo[0].get_repository_dir
        destination = repo[0].get_repository_dir.split(repo[0].name)[0] + request.data.get('name')

        if os.path.isdir(destination):
            raise serializers.ValidationError({'detail': '이미 존재하는 레포지토리가 있습니다.'})

        shutil.move(source, destination)
        repo.update(name=request.data.get('name'))

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        shutil.rmtree(instance.get_repository_dir)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ManagedFileCreateGenericAPIView(generics.CreateAPIView):
    queryset = ManagedFile.objects.all()
    serializer_class = ManagedFileSerializer


class ManagedFileRetrieveUpdateDestroyGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ManagedFile.objects.all()
    serializer_class = ManagedFileSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        repo = ManagedFile.objects.filter(pk=instance.pk)

        source = repo[0].file.path
        destination = repo[0].file.path.split(repo[0].name)[0] + request.data.get('name')

        if os.path.exists(destination):
            raise serializers.ValidationError({'detail': '이미 존재하는 파일이나 폴더가 있습니다.'})

        shutil.move(source, destination)
        repo.update(name=request.data.get('name'))

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.get_root_dir(instance) == instance:
            raise serializers.ValidationError({'detail': '루트 디렉터리는 삭제할 수 없습니다.'})
        if not instance.file:
            shutil.rmtree(
                os.path.join(
                    instance.get_root_dir(instance).root_repository.get_repository_dir,
                    instance.get_parent_dir(instance),
                    instance.name,
                )
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommitListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer

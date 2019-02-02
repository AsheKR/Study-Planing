from rest_framework import generics

from repository.apis.serializers import RepositorySerializer
from repository.models import Repository


class RepositoryListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer


class RepositoryRetrieveUpdateDestroyGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

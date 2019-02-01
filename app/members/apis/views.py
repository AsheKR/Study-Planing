from django.contrib.auth import get_user_model
from rest_framework import generics

from members.apis.serializers import UserCreateSerializer

User = get_user_model()


class UserCreateGenericAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

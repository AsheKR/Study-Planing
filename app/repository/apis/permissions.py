from rest_framework.permissions import BasePermission


class RepositoryPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True  # 해당 레포지토리에 대한 Retrieve 는 누구나 가능하다.
        return bool(
            request.method != 'PUT' and
            request.user.is_authenticated and
            obj.owner == request.user
        )

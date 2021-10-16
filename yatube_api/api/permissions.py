from rest_framework import permissions, status


class AuthorEditOrReadOnly(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH", "DELETE",)
    message = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if (obj.author == request.user and request.method
                in self.edit_methods):
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

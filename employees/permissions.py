from rest_framework.permissions import BasePermission


class IsAuthenticatedOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.user.is_superuser

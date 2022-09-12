from rest_framework import permissions


class RetrieveGuestPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if obj.hotel == request.user:
            return True

        return request.user.is_superuser

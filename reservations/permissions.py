from rest_framework import permissions


class RetrieveReservationPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if obj.room.hotel == request.user:
            return True

        return request.user.is_superuser

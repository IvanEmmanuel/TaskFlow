from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user_id", None) == request.user.id
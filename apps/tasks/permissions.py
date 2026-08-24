from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUser(BasePermission):
    """
    Permiso de nivel de objeto.

    Permite acceder al objeto únicamente cuando el usuario
    autenticado es el usuario relacionado con dicho objeto.
    """
    def has_object_permission(self, request, view, obj):
        # Comparamos el usuario propietario del objeto
        # con el usuario autenticado que realiza la petición.
        return getattr(obj, "user_id", None) == request.user.id
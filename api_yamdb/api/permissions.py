from rest_framework import permissions


class OnlyReadAndNotUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and not request.user.is_user
        )


class AdminPermission(permissions.BasePermission):
    """
    Проверка, что запрос от лица администратора
    или суперюзера.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )


class ModeratorPermission(permissions.BasePermission):
    """
    Проверка, что запрос от лица модератора
    или суперюзера.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or user.is_authenticated and not user.is_moderator
            or user.is_superuser
        )

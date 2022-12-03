from rest_framework import permissions


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

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )


class UserPermission(permissions.BasePermission):
    """
    Проверка, что запрос от лица обычного юзера
    или суперюзера.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_user
            or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.is_user
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
            user.is_authenticated and user.is_moderator
            or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.is_moderator
            or user.is_superuser
        )

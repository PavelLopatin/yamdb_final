from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_admin)
        ):
            return True
        return False


class GeneralPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_admin)
            or request.method in permissions.SAFE_METHODS
        ):
            return True
        return False


class ReviewOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
        ):
            return True

from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


# from apps.external_apps.models.app import App
#
#
# class AppPermission(BasePermission):
#     """
#     Allows access only to authenticated users.
#     """
#
#     def has_permission(self, request, view):
#         if isinstance(request.user, App):
#             return request.user.active
#         return False
class IsManager(BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_manager and request.user.is_authenticated


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_admin and request.user.is_authenticated


class IsUser(BasePermission):

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_user and request.user.is_authenticated

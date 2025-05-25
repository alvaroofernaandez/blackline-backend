from rest_framework.permissions import BasePermission


class IsNormalUser(BasePermission):

    def has_permission(self, request, view):

        if not request.user or not request.auth:
            return False

        token_data = request.auth

        if token_data.get('role') == 'user' or token_data.get('role') == 'admin':
            return True

        return False

class IsAdminUser(BasePermission):

    def has_permission(self, request, view):

        if not request.user or not request.auth:
            return False

        token_data = request.auth

        if token_data.get('role') == 'admin':
            return True

        return False
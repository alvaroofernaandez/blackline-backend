from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        token_data = request.auth
        print("Permiso IsAdminUser - token_data:", token_data)
        if not token_data:
            return False
        role = token_data.get('role')
        print("Role extraído del token:", role)
        return role == 'admin'


class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        token_data = request.auth
        print("Permiso IsNormalUser - token_data:", token_data)
        if not token_data:
            return False
        role = token_data.get('role')
        print("Role extraído del token:", role)
        return role in ['user', 'admin']
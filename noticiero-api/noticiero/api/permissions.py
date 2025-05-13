from rest_framework.permissions import BasePermission

class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        '''
        if not request.user or not getattr(request.user, 'is_authenticated', False):
            return False
        return request.user.get('role') in ['user', 'admin']
        '''

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        '''
        if not request.user or not getattr(request.user, 'is_authenticated', False):
            return False
        return request.user.get('role') == 'admin'
        '''

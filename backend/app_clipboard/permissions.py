from rest_framework import permissions

class IsClipboardOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return True
    
    def has_object_permission(self, request, view, obj):
        return obj.can_access(user=request.user, password=request.query_params.get('password', None))

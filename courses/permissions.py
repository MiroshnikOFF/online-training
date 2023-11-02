from rest_framework.permissions import BasePermission


class IsNotModeratorForAPIView(BasePermission):
    """Разрешает доступ к APIView всем кроме модераторов"""

    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderators'):
            return False
        return True


class IsNotModeratorForViewSet(BasePermission):
    """Разрешает доступ к create и destroy для ViewSet всем кроме модераторов"""

    def has_permission(self, request, view):
        if view.action in ['create', 'destroy']:
            if request.user.groups.filter(name='moderators'):
                return False
            return True
        return True


class IsOwner(BasePermission):
    """Разрешает доступ к объекту только владельцу или персоналу"""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner or request.user.is_staff:
            return True
        return False

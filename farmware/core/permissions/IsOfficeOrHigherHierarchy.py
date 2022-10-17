from rest_framework.permissions import BasePermission

from ..user.models import User


class IsHigherThanWorkerHierarchy(BasePermission):
    # for object level permissions
    def has_object_permission(self, request, view, user_obj):
        user: User = request.user

        # No user signed in
        if not user: return False

        # User is higher ranked than WORKER
        if user.role < User.Roles.WORKER: return True

        return False
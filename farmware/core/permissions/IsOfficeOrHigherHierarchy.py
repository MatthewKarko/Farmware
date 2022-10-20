from rest_framework.permissions import BasePermission

from ..user.models import User


class IsHigherThanWorkerHierarchy(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user

        # No user signed in
        if not user: return False

        # User is higher ranked than WORKER
        if user.role < User.Roles.WORKER: return True

        return False
from rest_framework.permissions import BasePermission

from .models import User

class IsInOrganisation(BasePermission):
    # # for view permission
    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, user_obj):
        return request.user and (
            request.user.organisation == user_obj.organisation)

class IsInHierarchy(BasePermission):
    """
    Impose a hierarchy permission system.

    - All ADMINS should not be able to edit anything below. 
    - All roles below ADMIN should not be able to edit, unless it is themselves.
    """
    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, user_obj):
        print(User.Roles.ADMIN)
        user: User = request.user
        # No user signed in.
        if not user: return False

        # User should be able to edit themselves
        if user == user_obj: return True

        # User signed in is not an ADMIN or higher
        if request.user.role > User.Roles.ADMIN: return False

        # Ensure hierarchy
        return request.user.role < user_obj.role
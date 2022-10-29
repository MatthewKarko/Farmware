from rest_framework.permissions import BasePermission

from .models import User
from ..api.models.order import OrderItemStockLink

class IsInOrganisation(BasePermission):

    mappings = {
        OrderItemStockLink: 'stock_id'
    }

    # for object level permissions
    def has_object_permission(self, request, view, obj):
        if request.user is None: return False

        mapping_item = self.mappings.get( type(obj), None )
        if mapping_item is not None:
            organisation = getattr(obj, mapping_item).organisation
        else:
            organisation = obj.organisation

        return request.user.organisation == organisation

class UserHierarchy(BasePermission):
    """
    Impose a hierarchy permission system.

    - All ADMINS should be able to edit anything below. 
    - All roles below ADMIN should not be able to edit, unless it is themselves.
    """
    def has_object_permission(self, request, view, user_obj):
        user: User = request.user
        # No user signed in
        if not user: return False

        # User should be able to edit themselves
        if user == user_obj: return True

        # User is NOT an ADMIN or HIGHER
        if user.role > User.Roles.ADMIN: return False

        # Ensure hierarchy
        return user.role <= user_obj.role

class OnlyYou(BasePermission):
    """Only you have permissions."""
    def has_object_permission(self, request, view, user_obj):
        user: User = request.user

        # User should be able to edit themselves
        return user and (user == user_obj)

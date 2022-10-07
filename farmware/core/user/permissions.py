from rest_framework.permissions import BasePermission

class IsInOrganisation(BasePermission):
    # # for view permission
    # def has_permission(self, request, view):
    #     return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, user_obj):
        return request.user and (
            request.user.organisation == user_obj.organisation)
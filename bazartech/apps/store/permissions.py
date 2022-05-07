from rest_framework.permissions import SAFE_METHODS, BasePermission


class OwnProductPermission(BasePermission):
    """
    Object-level permission to only allow updating his own profile
    or if the updater is a superuser
    """

    def has_object_permission(self, request, view, object):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        return object.owner == request.user or request.user.is_superuser

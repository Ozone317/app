from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow a user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check if the user is trying to edit their own profile"""

        # If the user is making a request that does not change the data inside the database, then simply allow them.
        # In other words, if the user has made a safe request, then allow it.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Otherwise, we need to check if the user who is trying to edit the data is actually the owner of the said data.
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow a user to edit their own status"""

    def has_object_permission(self, request, view, obj):
        """Check if the user is trying to edit their own status"""

        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Otherwise check the ID of the user.
        # Object (obj) here is ProfileFeedItem
        return obj.user.id == request.user.id
from rest_framework.permissions import BasePermission

# is staff premition
class IsStaffUser(BasePermission):
    """
    Custom permission to only allow staff users to add, update, or delete products.
    """

    def has_permission(self, request, view):
        # Only allow staff users to add, update, or delete products
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_staff
        return True

# user cart premition   
class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of a cart item to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Object-level permission: Only allow access if the cart item belongs to the user
        return obj.user == request.user
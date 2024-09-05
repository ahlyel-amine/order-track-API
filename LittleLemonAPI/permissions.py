from rest_framework.permissions import BasePermission


class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=['Delivery Crew']).exists()

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=['Customer']).exists()

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()


class IsCustomerOrDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name__in=['Customer', 'Delivery Crew']).exists()

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only methods for all authenticated users
        if request.method in ['GET']:
            return request.user and request.user.is_authenticated
        # Allow write methods only for managers
        return request.user and request.user.groups.filter(name='Manager').exists()
    


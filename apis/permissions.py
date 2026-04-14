from rest_framework import permissions

class CostumPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.phone == "09166667777"
    
    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user
class AnotherCostumPerm(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.name == "moz"   

from rest_framework.throttling import ScopedRateThrottle


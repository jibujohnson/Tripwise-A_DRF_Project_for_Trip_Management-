from rest_framework.permissions import BasePermission

class OwnerOnly(BasePermission):
    def has_object_permission(self,request,obj):
        return request.user==obj.created_by
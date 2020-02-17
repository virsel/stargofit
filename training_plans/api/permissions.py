from rest_framework.permissions import BasePermission

class IsSelected(BasePermission):
    # this method returns True to grant access or False
    # check that user performing request is present in the consumers relationship of Training_plan object
    def has_object_permission(self,request,view,obj):
        return obj.consumers.filter(id=request.user.id).exists()
        

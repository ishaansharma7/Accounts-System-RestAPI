from rest_framework import permissions

class IsTransactionUser(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        print('obj.user: ',obj.user)
        print('request.user', request.user)
        return  obj.user == request.user
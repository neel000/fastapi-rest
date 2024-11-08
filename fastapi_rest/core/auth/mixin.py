from fastapi import status
from fastapi.responses import JSONResponse
from ..views.base_views import MethodMapper

class AuthMixin:
    authentication_class = []
    
    def is_authenticated(self):
        if not self.authentication_class:
            return True
        
        for _class in self.authentication_class:
            if _class(self).has_authentication():
                return True
            
        return False

class PermissionMixin:
    permission_class = []
    def is_permission(self):
        if not self.permission_class:
            return True
        
        for _class in self.permission_class:
            if _class(self).has_permission():
                return True
            
        return False

class AccessMixin(AuthMixin, PermissionMixin, MethodMapper):
    def __is_access(self):
        if not self.is_authenticated():
            return JSONResponse(
                content={"message":"Authentication Required"}, 
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        if not self.is_permission():
            return JSONResponse(
                content={"message":"Permission Denied"}, 
                status_code=status.HTTP_403_FORBIDDEN
            )

        return True 
    
    async def main(self):
        if not self.__is_access() == True:
            return self.__is_access()
            
        methods_list = self.methods_mapper()
        return await methods_list[self.request.method]()
    

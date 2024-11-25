from fastapi_rest.responses import status
from fastapi_rest.request.method_mapper import MethodMapperMixin 

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

class IsAccessMixin:
    def _is_access(self):
        if not self.is_authenticated():
            self.status_code = status.HTTP_401_UNAUTHORIZED
            return {"message":"Authentication Required"}

        if not self.is_permission():
            self.status_code=status.HTTP_403_FORBIDDEN
            return {"message":"Permission Denied"}
                
        return True

class Construct(AuthMixin, PermissionMixin, MethodMapperMixin, IsAccessMixin):...
    
class AccessMixin(Construct):
    def main(self):
        if not self._is_access() == True:
            return self._is_access()
        methods_list = self.methods_mapper()
        return methods_list[self.request.method]() 

class AsyncAccessMixin(Construct):
    async def main(self):
        if not self._is_access() == True:
            return self._is_access()
        methods_list = self.methods_mapper()
        return await methods_list[self.request.method]()
    

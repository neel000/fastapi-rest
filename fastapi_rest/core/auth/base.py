from abc import ABC, abstractmethod
class BaseAuthentication(ABC):
    def __init__(self, class_self):
        self.view_class = class_self
        pass
    
    @abstractmethod
    def has_authentication(self)->bool:
        return False

class BasePermission(ABC):
    def __init__(self, class_self):
        self.view_class = class_self
    
    @abstractmethod
    def has_permission(self)->bool:
        return False
    
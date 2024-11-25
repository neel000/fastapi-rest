class MethodMapperMixin:

    @staticmethod
    def keys():
        return ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
    
    def methods_mapper(self):
        func_list = {}
        for method in self.keys():
            func_list[method] = getattr(self, method.lower())
        return func_list
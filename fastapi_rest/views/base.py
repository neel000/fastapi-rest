from .mixin import Construct

class View(Construct):
    def get(self):
        return self.default_response("GET")

    def post(self):
        return self.default_response("POST")
    
    def put(self):
        return self.default_response("PUT")
    
    def patch(self):
        return self.default_response("PATCH")

    def delete(self):
        return self.default_response("DELETE")
    
    def options(self):
        return self.default_response("OPTIONS")
    
    def head(self):
        return self.default_response("HEAD")

    def main(self):
        methods_list = self.methods_mapper()
        return methods_list[self.request.method]()

class AsyncView(Construct):
    
    async def get(self):
        return self.default_response("GET")

    async def post(self):
        return self.default_response("POST")
    
    async def put(self):
        return self.default_response("PUT")
    
    async def patch(self):
        return self.default_response("PATCH")

    async def delete(self):
        return self.default_response("DELETE")
    
    async def options(self):
        return self.default_response("OPTIONS")
    
    async def head(self):
        return self.default_response("HEAD")

    async def main(self):
        methods_list = self.methods_mapper()
        return await methods_list[self.request.method]()
    

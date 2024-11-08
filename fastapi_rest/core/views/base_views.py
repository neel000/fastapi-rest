from fastapi.responses import JSONResponse
from fastapi import status

class MethodMapper:
    def methods_mapper(self):
        return {
            "GET":self.get,
            "POST":self.post,
            "PUT":self.put,
            "PATCH":self.patch,
            "DELETE":self.delete,
            "HEAD":self.head,
            "OPTIONS":self.options
        }

class View(MethodMapper):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.status_code = status.HTTP_200_OK
        self.headers = {}
    
    def default_response(self, method):
        self.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return JSONResponse(content=f"//{method} Method is not allowed.//", status_code=self.status_code)
    
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


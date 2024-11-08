from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse, JSONResponse
import os

methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

def request_handle(cls):
    async def wrapper(request:Request):
        class_name = cls(request=request, **request.path_params)
        resp = await class_name.main()

        if resp.__class__ == JSONResponse:
            return resp
        
        if resp is None:
            return Response(status_code=class_name.status_code)
        return JSONResponse(content=resp, status_code=class_name.status_code)
    
    return wrapper

def handle_media(path):
    async def wrapper(request:Request):
        params = request.path_params
        folder = params.get("folder", "")
        filename = params.get("filename", "")
        file_path = os.path.join(path, folder, filename)
        
        if not os.path.isfile(file_path):
            return JSONResponse(content={"message":"File is not found"} ,status_code=404)
        
        return FileResponse(file_path)
    
    return wrapper

def url(path, func,  methods=methods_list):
    path = path.replace("<", "{").replace(">", "}")
    return [path, func, methods]

def class_url(path, func, methods=methods_list):
    func = request_handle(func)
    return url(path, func, methods)

def setup_path(urls, router):
    for _url in urls:
        router.add_route(*_url)
    
def include(prefix, urls):
    for i in urls:
        i[0] = prefix+i[0]
    return urls

class DefaultRouter:
    __pathlist = []

    def register(self, path, func, methods=methods_list):
        self.__pathlist.append(class_url(path, func, methods=["GET", "POST"]))
        path = f"{path}/<instance>"
        self.__pathlist.append(class_url(path, func, methods=["GET", "PUT", "DELETE", "PATCH"]))

    @property
    def routes(self):
        return self.__pathlist


media_url = lambda path:[
    url("/{filename}", func=handle_media(path), methods=["GET"]),
    url("/{folder:path}/{filename}", func=handle_media(path), methods=["GET"])
]
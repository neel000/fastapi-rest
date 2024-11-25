from fastapi_rest.responses import handle_response, handle_async_response
from fastapi_rest.request.method_mapper import MethodMapperMixin
import inspect

methods_list = MethodMapperMixin.keys()

def include(prefix, urls):
    for i in urls:
        i[0] = prefix+i[0]
    return urls

def setup_path(app, url_patterns):
    for i in url_patterns:
        app.add_route(*i)

def path(url, func,  methods=methods_list):
    url = url.replace("<", "{").replace(">", "}")
    return [url, func, methods]

def class_path(url, cls, methods=methods_list):
    func = (
        handle_async_response(cls) 
        if inspect.iscoroutinefunction(cls.main) 
        else handle_response(cls)
    )
    return path(url, func, methods)

class DefaultRouter:
    __pathlist = []

    def register(self, path, func):
        self.__pathlist.append(class_path(path, func, methods=["GET", "POST"]))
        path = f"{path}/<pk>"
        self.__pathlist.append(class_path(path, func, methods=["GET", "PUT", "DELETE", "PATCH"]))

    @property
    def urls(self):
        return self.__pathlist
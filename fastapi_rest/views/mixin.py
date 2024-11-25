from fastapi import status
from fastapi_rest.request.method_mapper import MethodMapperMixin

class DefaultResponseMixin:
    def default_response(self, method):
        self.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return f"//{method} Method is not allowed.//"

class Construct(MethodMapperMixin, DefaultResponseMixin):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.status_code = status.HTTP_200_OK
        self.headers = {}


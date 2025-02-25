from fastapi.responses import JSONResponse
from fastapi import Response as Resp
from fastapi.encoders import jsonable_encoder

class Response:
    def __new__(cls, data=None, status_code:int=200):
        if data is None:
            return Resp(status_code=status_code)
        return JSONResponse(content=jsonable_encoder(data), status_code=status_code)

def handle_response(cls):
    def wrapper(request):
        class_name = cls(request=request, **request.path_params)
        resp = class_name.main()
        return Response(data=resp, status_code=class_name.status_code)
    return wrapper

def handle_async_response(cls):
    async def wrapper(request):
        class_name = cls(request=request, **request.path_params)
        resp = await class_name.main()
        return Response(data=resp, status_code=class_name.status_code)
    return wrapper
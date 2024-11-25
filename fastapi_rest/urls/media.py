from fastapi_rest.responses import Response, FileResponse
from .path import path as url
import os

def handle_media(path):
    def wrapper(request):
        params = request.path_params
        folder = params.get("folder", "")
        filename = params.get("filename", "")
        file_path = os.path.join(folder, filename)

        if not file_path.startswith(path):
            return Response(data={"message":"Not found!"} ,status_code=404)
        
        if not os.path.isfile(file_path):
            return Response(data={"message":"File is not found"} ,status_code=404)
        return FileResponse(file_path)
    
    return wrapper

media_url = lambda path:[
    url("/{filename}", func=handle_media(path), methods=["GET"]),
    url("/{folder:path}/{filename}", func=handle_media(path), methods=["GET"])
]
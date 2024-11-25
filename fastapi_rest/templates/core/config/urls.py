from fastapi_rest.urls import setup_path, include
from fastapi_rest.urls.media import media_url
from .settings import MEDIA_DIR, MEDIA_PATH
from fastapi import APIRouter

root_router = APIRouter()

url_patterns = [
    *include(MEDIA_PATH, media_url(MEDIA_DIR))
]

setup_path(root_router, url_patterns)


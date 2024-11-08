from fastapi_rest.core.conf.urls import media_url, setup_path, include
from .settings import MEDIA_DIR, MEDIA_PATH
from fastapi import APIRouter

root_router = APIRouter()

url_patterns = [
    *include(MEDIA_PATH, media_url(MEDIA_DIR))
]

setup_path(url_patterns, root_router)


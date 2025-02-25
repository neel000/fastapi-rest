from fastapi_rest.urls import path, setup_path, include, DefaultRouter, class_path
from fastapi import APIRouter
root_router = APIRouter()
from .import views

viewset_router = DefaultRouter()

viewset_router.register("/viewset", views.TestModelViewSet)
viewset_router.register("/async-viewset", views.TestAsyncModelViewSet)

home_url = [
    path("/", views.home),
    path("/async-view", views.async_view),
    path("/session-test", views.session_test),
    path("/async-session-test", views.async_session_test),
    class_path("/create-test", views.TestCreateView),
    class_path("/update-test/<pk>", views.TestUpdateView),
    *include("", viewset_router.urls),
]

url_patterns = [
    *include("", home_url),
]

setup_path(root_router, url_patterns)


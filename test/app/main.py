from fastapi import FastAPI
from app.urls import root_router

app = FastAPI()
routers = [root_router]

for router in routers:
    app.include_router(router, dependencies=[])
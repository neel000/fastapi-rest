from fastapi import FastAPI
from fastapi import FastAPI, Request, HTTPException
from fastapi_rest.responses import Response
import logging
from config.urls import root_router

app = FastAPI()

def middleware():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    @app.middleware("http")
    async def error_handling_middleware(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exception:
            logger.error(f"HTTPException: {http_exception.detail}")
            return Response(
                status_code=http_exception.status_code,
                data={"detail": http_exception.detail},
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                status_code=500,
                data={"detail": "An unexpected error occurred."},
            )

middleware()

routers = [root_router]

for router in routers:
    app.include_router(router, dependencies=[])


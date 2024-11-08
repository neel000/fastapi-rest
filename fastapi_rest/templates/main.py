from fastapi import FastAPI
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
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
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"detail": http_exception.detail},
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "An unexpected error occurred."},
            )

middleware()
routers = [root_router]

for router in routers:
    app.include_router(router, dependencies=[])


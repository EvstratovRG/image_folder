from typing import Callable

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from application import api, settings
from application.db.session import SessionLocal
from application.loaders import pre_load_all_models


app = FastAPI(
    title=settings.SERVICE_NAME,
    docs_url=f"{settings.API_BASE_URL}/swagger/",
)


_allow_all = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=settings.CORS_ORIGINS,
    allow_headers=settings.CORS_ORIGINS,
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next: Callable) -> Response:
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        await request.state.db.close()
    return response


app.include_router(api.router, prefix=settings.API_BASE_URL)

pre_load_all_models()

# raise Exception(settings.SERVER_HOST, settings.SERVER_PORT)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        loop="uvloop",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )

from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from api import posts_router

app = FastAPI()

@app.get("/", response_class=RedirectResponse)
def index():
    return "/docs"

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code" : f"{exc.code}", "message" : f"{exc.name}"}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        # content={"code" : f"{exc.code}", "message" : f"{exc.name}"}
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )

app.include_router(posts_router.router)
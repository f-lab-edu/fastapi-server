from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.exceptions import HTTPException

from API import post_router

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

app.include_router(post_router.router)
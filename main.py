from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api import api_router
from database import SQLModel, engine

SQLModel.metadata.create_all(engine)
app = FastAPI()


@app.get("/", response_class=RedirectResponse)
def index():
    return "/docs"


app.include_router(api_router.router)

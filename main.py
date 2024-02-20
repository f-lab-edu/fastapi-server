from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api import posts_router
from database import engine, SQLModel

SQLModel.metadata.create_all(engine)
app = FastAPI()

@app.get("/", response_class=RedirectResponse)
def index():
    return "/docs"

app.include_router(posts_router.router)
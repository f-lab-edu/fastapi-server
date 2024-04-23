from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api import comment, post, user
from database import SQLModel, engine

SQLModel.metadata.create_all(engine)
app = FastAPI()


@app.get("/", response_class=RedirectResponse)
async def index():
    return "/docs"


app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)

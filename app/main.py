from fastapi import FastAPI
from typing import Union
from fastapi.templating import Jinja2Templates
from .routers import keywords, news, rss

app = FastAPI()



app.include_router(rss.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
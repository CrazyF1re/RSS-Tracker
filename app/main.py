from fastapi import FastAPI
from typing import Union
from fastapi.templating import Jinja2Templates
from .routers import keywords, news, rss
from dotenv import load_dotenv


app = FastAPI()

# Load .env file
load_dotenv()


app.include_router(rss.router)
app.include_router(keywords.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
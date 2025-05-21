from fastapi import FastAPI, Request
from typing import Union
from .routers import keywords, news, rss
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Load .env file
load_dotenv()


app.include_router(rss.router)
app.include_router(keywords.router)
app.include_router(news.router)

templates = Jinja2Templates(directory="./app/templates")

@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse(request=request, name="main.html")

from fastapi import FastAPI, Request
from .routers import keywords, news, rss
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import os
import requests
import xml.etree.ElementTree as ET
# Load .env file
load_dotenv()

def update_news():
    con = sqlite3.connect(os.environ["DB_NAME"])
    rss_list = con.cursor().execute("""SELECT * from rss""").fetchall()
    rss_list = [i[0] for i in rss_list]
    for url in rss_list:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        lst = []
        tree = ET.ElementTree(ET.fromstring(resp.text))
        for i in tree.findall(".//channel/item"):
            title = i.find("title").text
            link = i.find("link").text
            magazin = url.split('.ru')[0]+".ru"
            lst.append((title,magazin,link))
        con.cursor().executemany("""insert or ignore into news(title,magazin,url) values(?,?,?)""",lst)
        con.commit()
    con.close()
    


@asynccontextmanager
async def lifespan(app:FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_news,"interval",minutes = 1)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)






app.include_router(rss.router)
app.include_router(keywords.router)
app.include_router(news.router)

templates = Jinja2Templates(directory="./app/templates")

@app.get("/")
def read_root(request:Request):
    return templates.TemplateResponse(request=request, name="news.html")

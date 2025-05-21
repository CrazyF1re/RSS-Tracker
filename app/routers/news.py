from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from ..dependencies import get_session
from pydantic import BaseModel
from DataCollection.collection import Database

class Item(BaseModel):
    url:str

class ListItem(BaseModel):
    list:list[str]

router =  APIRouter(
    prefix="/news"
)

templates = Jinja2Templates(directory="./app/templates")

@router.get("")
def get_rss_list(request:Request, session:Database = Depends(get_session)):
    list = session.get_news_list()
    list = [{"id":list.index(i),"title":i[0], "magazin": i[1], "url":i[2]} for i in list]
    keywords_list = session.get_keywords_list()
    return templates.TemplateResponse(request=request, name="news.html", context={"list":list, "keywords":keywords_list})
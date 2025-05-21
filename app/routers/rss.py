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
    prefix="/rss"
)

templates = Jinja2Templates(directory="./app/templates")

@router.get("")
def get_rss_list(request:Request, session:Database = Depends(get_session)):
    list = session.get_rss_list()
    list = [{"id":list.index(i),"rss":i[0]} for i in list]
    return templates.TemplateResponse(request=request, name="rss.html", context={"list":list})

@router.put("")
def add_rss(item: Item, session:Database = Depends(get_session)):
    session.add_rss(item.url)
    
@router.delete("")
def delete_choosen_rss(list:ListItem,session:Database = Depends(get_session)):
    session.del_rss(list.list)

@router.post("")
def setup_default_rss(session:Database = Depends(get_session)):
    session.setup_default_rss()
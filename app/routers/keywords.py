from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from ..dependencies import get_session
from pydantic import BaseModel
from DataCollection.collection import Database

class ListItem(BaseModel):
    list:list[str]

router =  APIRouter(
    prefix="/keywords"
)

templates = Jinja2Templates(directory="./app/templates")

@router.get("")
def get_keywords_list(request:Request, session:Database = Depends(get_session)):
    list = session.get_keywords_list()
    list = [{"id":list.index(i),"rss":i[0]} for i in list]
    return templates.TemplateResponse(request=request, name="keywords.html", context={"list":list})

@router.put("")
def add_keywords(list:ListItem, session:Database = Depends(get_session)):
    if len(list.list):
        session.add_keywords(list.list)
    
@router.delete("")
def delete_choosen_keywords(list:ListItem,session:Database = Depends(get_session)):
    if len(list.list):
        session.del_keywords(list.list)

@router.post("")
def setup_default_keywords(session:Database = Depends(get_session)):
    session.setup_default_keywords()
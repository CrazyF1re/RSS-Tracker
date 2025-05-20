from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi import Depends
import sqlite3
from ..dependencies import get_session
from pydantic import BaseModel

class Item(BaseModel):
    url:str

class ListItem(BaseModel):
    list:list[str]

router =  APIRouter(
    prefix="/rss"
)

templates = Jinja2Templates(directory="./app/templates")

@router.get("")
def get_rss_list(request:Request, session:sqlite3.Connection = Depends(get_session)):
    list = session.cursor().execute("""SELECT * from rss""").fetchall()
    list = [{"id":list.index(i),"rss":i[0]} for i in list]
    return templates.TemplateResponse(request=request, name="rss.html", context={"list":list})

@router.put("")
def add_rss(item: Item, session:sqlite3.Connection = Depends(get_session)):

    
    session.cursor().execute("""INSERT OR IGNORE INTO rss values(?)""",(item.url,))
    session.commit()
    return {"This is response to put request":"",**item.model_dump()}
    

@router.delete("")
def delete_choosen_rss(list:ListItem,session:sqlite3.Connection = Depends(get_session)):
    session.cursor().executemany("""DELETE FROM rss WHERE url = ?""", [(i,) for i in list.list])
    session.commit()
    
    return {"This is response to delete request":"","lst":list}
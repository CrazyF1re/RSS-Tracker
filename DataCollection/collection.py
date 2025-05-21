#mysql
import sqlite3
import requests
import os
import json
from pymystem3 import Mystem
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Load .env file
load_dotenv()
RSS = json.loads(os.environ['RSS'])
KEYWORDS = json.loads(os.environ['KEYWORDS'])
DB_NAME = os.environ["DB_NAME"]


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class Database:
    def __init__(self):
        self.__con = sqlite3.connect(DB_NAME)
        self.__cur = self.__con.cursor()
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS news (
            title text PRIMARY KEY, 
            magazin text NOT NULL, 
            url text NOT NULL
        );""")

        self.__cur.execute("""CREATE TABLE IF NOT EXISTS rss(
            url text NOT NULL UNIQUE
                         )""")
        
        self.__cur.execute("""CREATE TABLE IF NOT EXISTS keywords(
            word text NOT NULL UNIQUE        
        )""")
        self.__con.commit()

    def __get_news_rss(self,url):
        print(url)
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        lst = []
        tree = ET.ElementTree(ET.fromstring(resp.text))
        for i in tree.findall(".//channel/item"):
            title = i.find("title").text
            link = i.find("link").text
            magazin = url.split('.ru')[0]+".ru"
            lst.append((title,magazin,link))
        self.__cur.executemany("""insert or ignore into news(title,magazin,url) values(?,?,?)""",lst)
        self.__con.commit()
    
    def __del_news_rss(self,url):
        magazin = url.split('.ru')[0]+".ru"
        self.__cur.execute("""DELETE FROM news WHERE  magazin = ?""", (magazin,))
        self.__con.commit()

    def add_rss(self, rss:str):
        self.__cur.execute("""INSERT OR IGNORE INTO rss values(?)""",(rss,))
        self.__con.commit()
        self.__get_news_rss(rss)

    def del_rss(self, rss:list):
        self.__cur.executemany("""DELETE FROM rss WHERE url = ?""", [(i,) for i in rss])
        self.__con.commit()
        for i in rss:
            self.__del_news_rss(i)
    
    def setup_default_rss(self):
        cur_rss  = [i[0] for i in self.get_rss_list()]
        for i in RSS:
            if i not in cur_rss:
                self.__get_news_rss(i)
        tmp = [(i,) for i in RSS]
        self.__cur.executemany("""INSERT OR IGNORE INTO rss values(?)""",tmp)
        self.__con.commit()

    def get_rss_list(self):
        return self.__cur.execute("""SELECT * from rss""").fetchall()
    
    def get_keywords_list(self):
        return self.__cur.execute("""SELECT * from keywords""").fetchall()
    
    def setup_default_keywords(self):
        tmp = [(i,) for i in KEYWORDS]
        self.__cur.execute("""DELETE FROM keywords""")
        self.__cur.executemany("""INSERT OR IGNORE INTO keywords values(?)""",tmp)
        self.__con.commit()

    def add_keywords(self, keywords:list):
        self.__cur.executemany("""INSERT OR IGNORE into keywords values(?)""",[(i,) for i in keywords])
        self.__con.commit()

    def del_keywords(self, keywords:list):
        self.__cur.executemany("""DELETE FROM keywords where word = ?""",[(i,) for i in keywords])
        self.__con.commit()

    def get_news_list(self):
        keywords_list = [i[0] for i in self.get_keywords_list()]
        news_list = self.__cur.execute("""SELECT * from news""").fetchall()
        str_news =[str(i[0] + "||") for i in news_list]
        m = Mystem()
        counter = 0
        list_of_numbers = []
        for i in m.lemmatize(''.join(str_news)):
            if "||" in i:
                counter +=1
            if i.capitalize() in keywords_list:
                list_of_numbers.append(counter)
        res = []
        for i in list_of_numbers:
            res.append(news_list[i])
        return res
        

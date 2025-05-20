#mysql
from config import *
import sqlite3
import requests
import os
import xml.etree.ElementTree as ET
import time

class Database:
    def __init__(self):
        self.con = sqlite3.connect(DB_NAME)
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS news (
            title text PRIMARY KEY, 
            magazin text NOT NULL, 
            url text NOT NULL
        );""")

    def get_news(self):
        lst = []
        for blog in RSS:
            print(blog)
            resp = requests.get(blog)
            time.sleep(1)
            tree = ET.ElementTree(ET.fromstring(resp.text))
            for i in tree.findall(".//channel/item"):
                title = i.find("title").text
                link = i.find("link").text
                magazin = blog.split('.ru')[0]+".ru"
                lst.append((title,magazin,link))
        self.cur.executemany("""insert or ignore into news(title,magazin,url) values(?,?,?)""",lst)
        self.con.commit()
            
            
        


def main():
    a = Database()
    a.get_news()
    
if __name__ == "__main__":
    main()
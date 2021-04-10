from bs4 import BeautifulSoup
import requests
import time

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="bhumit",
  password="admin123",
  database="novels"
)

url = "https://www.webnovel.com/book/the-crown's-obsession_17319692206490105"


def create(data):
    global mydb
    mycursor = mydb.cursor()
    sql = "INSERT INTO chapters(novelID,chapterno,chapter_title,chapter_link) VALUES (%s,%s,%s,%s)"
    mycursor.executemany(sql, data)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def get_chapter(novelID,url):
    session = requests.Session()
    page_data = session.get(url).text
    soup = BeautifulSoup(page_data, 'lxml')
    data = []
    table_data = soup.find('table',id="chapters").find_all('td',class_ = False)
    chapter_no = 1
    for tab in table_data:
        chapter = tab.text.split()
        chapter_title = ' '.join(chapter)
        chapter_link = "www.royalroad.com" + tab.find('a',href= True)["href"]
        data.append((novelID,chapter_no,chapter_title,chapter_link))
        chapter_no += 1
    create(data)


def scrap_chapters():
    global mydb
    mycursor = mydb.cursor()
    session = requests.Session()
    mycursor.execute("select novelID,url from test where novelID not in (select novelID from chapters)and url like '%royalroad.com%';")
    myresult = mycursor.fetchall()
    for novels in myresult:
        get_chapter(novels[0], novels[1])
        print("chapters inserted for: ", novels[0])

scrap_chapters()

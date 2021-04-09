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
    url = url + "/catalog"
    page_data = requests.get(url).text
    soup = BeautifulSoup(page_data, 'lxml')
    chapter_title = soup.find( 'div', class_="j_catalog_list" ).find_all( 'a' )
    data = []
    if chapter_title[0].text.split()[0]!= '1' or chapter_title[0].text.split()[0]!= '0':
        chapter_title.pop(0)
    for chapters in chapter_title:
        t = chapters.text.split()
        no = int(t[0])
        title = ' '.join(t[1:-2])
        link = chapters["href"].lstrip("//")
        data.append((novelID, no, title, link))
    create(data)


def scrap_chapters():
    global mydb
    mycursor = mydb.cursor()
    session = requests.Session()
    mycursor.execute("select novelID,url from test where novelID not in (select novelID from chapters)and url like '%webnovel.com%';")
    myresult = mycursor.fetchall()
    for novels in myresult[:10]:
        get_chapter(novels[0], novels[1])
        print("chapters inserted for: ", novels[0])

scrap_chapters()


from bs4 import BeautifulSoup
import requests
import random

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="bhumit",
  password="admin123",
  database="novels"
)

url = "https://www.royalroad.com/fictions/best-rated?page="

def update(title,url,chapters,author,genre,about,img):
    global mydb
    mycursor = mydb.cursor()
    sql = "INSERT INTO novelsdetails (title, url, author, chapters, description, image, genre) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (title,url,author,chapters,about,img,genre)
    mycursor.execute(sql, val)
    mydb.commit()
    #print(mycursor.rowcount, "record inserted.")



def create(title,url):
    global mydb
    mycursor = mydb.cursor()
    sql = "INSERT INTO test (title, url) VALUES (%s, %s)"
    val = (title,url)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def update_details():
    global mydb
    mycursor = mydb.cursor()
    mycursor.execute("select title,url from test where url not in (select url from novelsdetails) and url like '%royalraod.com%';")
    myresult = mycursor.fetchall()

    for novels in myresult:
        title,url = novels
        tag_list = []
        page = requests.get(url).text
        soup = BeautifulSoup(page,'lxml')
        #novel_object = soup.find('div',class_ = 'col-md-3 hidden-sm hidden-xs text-center')
        image = soup.find('div',class_ = 'col-md-3 hidden-sm hidden-xs text-center').find('img',src = True)["src"]
        tags = soup.find('span',class_ = 'tags').find_all('a',class_ = "label label-default label-sm bg-blue-dark fiction-tag")
        for tag in tags:
            tag_list.append(tag.text)
        if len(tag_list) == 0:
            tag_list = ["Action"]
        genre = random.choice(tag_list)
        chapters = int(soup.find('table',id = "chapters")["data-chapters"])
        author = soup.find('h4').find_all('span')[1].text.strip("\n")
        description = (soup.find('div',class_ = "hidden-content").text.strip("\n"))[0:4950] + "..."
        update(title,url,chapters,author,genre,description,image)
        print("details inserted for: ", title)


def scrap_novels(n):
    global url
    for pageno in range(1,n+1):
        page_url = url + str(pageno)
        page_data = requests.get(page_url).text
        print("pageno:" + str(pageno) + " Scrapped")
        soup = BeautifulSoup(page_data,'lxml')
        novel_object = soup.find_all('h2',class_ = 'fiction-title')
        for title in novel_object:
            add = "https://www.royalroad.com" + title.find('a',href = True)["href"]
            title = title.text.lstrip("\n").rstrip("\n")
            create(title,add)

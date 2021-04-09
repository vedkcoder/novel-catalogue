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

url = "https://www.webnovel.com/category/0_novel_page"

def update(title,url,chapters,author,genre,about,img):
    global mydb
    mycursor = mydb.cursor()
    sql = "INSERT INTO novelsdetails (title, url, author, chapters, description, image, genre) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (title,url,author,chapters,about,img,genre)
    mycursor.execute(sql, val)
    mydb.commit()



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
    mycursor.execute("select title,url from test where url not in (select url from novelsdetails) and url like '%webnovel.com%';")
    myresult = mycursor.fetchall()
    for novels in myresult:
        title,url = novels
        page = requests.get(url).text
        soup = BeautifulSoup(page,'lxml')
        novel_object = soup.find('div',class_ = 'det-info g_row c_000 fs16 pr')
        image = "https:" + novel_object.find('img',src = True)["src"]
        genre = novel_object.find('a',title = True)["title"]
        try:
            chapters =  int(novel_object.find('p',class_="mb12 lh24 det-hd-detail c_000 fs0").find_all('span')[-2].text.replace(" Chapters","").replace(",",""))
        except ValueError:
            chapters = 0
        author = novel_object.find('p',class_ = "ell dib vam").text.lstrip("Author: ").split("Translator")[0]
        try:
            description = (str(soup.find_all('p',class_="c_000")[2]).replace("<br/>","\n").replace('<p class="c_000">','').replace('</p>',''))[0:4950] + "..."
        except IndexError:
            description = "No description"
        update(title,url,chapters,author,genre,description,image)
        print("details inserted for: ", title)

def scrap_novels(n):
    global url
    for pageno in range(1,n+1):
        #time.sleep()
        page_url = url + str(pageno)
        page_data = requests.get(page_url).text

        print("pageno:" + str(pageno) + " Scrapped")

        soup = BeautifulSoup(page_data,'lxml')
        novel_object = soup.find_all('h3',class_ = 't_sub1 ell mb4')

        for title in novel_object:
            add = "https://www.webnovel.com" + title.find('a',href = True)["href"]
            create(title.text,add)

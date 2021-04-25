from django.shortcuts import render
from django.http import HttpResponse
from .models import novels,chapter
import mysql.connector
# Create your views here.
def home(request):
    mydb = mysql.connector.connect(
    host="localhost",
    user="bhumit",
    password="admin123",
    database="novels"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select novelID,title,image,author,genre,url from novelsdetails where novelID < 50;")
    myresult = mycursor.fetchall()
    novelss = []
    for results in myresult:
        novel = novels()
        novel.id = results[0]
        novel.title = results[1]
        novel.img = results[2]
        novel.author = results[3]
        novel.genre = results[4]
        novel.link = results[5]
        novelss.append(novel)
    return render(request,'home.html',{'novels':novelss})
    

def details(request):
    mydb = mysql.connector.connect(
    host="localhost",
    user="bhumit",
    password="admin123",
    database="novels"
    )
    novelid = request.GET['id']
    mycursor = mydb.cursor()
    mycursor.execute("select novelID,title,image,author,genre,url,description,chapters from novelsdetails where novelID = "+novelid+";")
    results = mycursor.fetchall()[0]
    novel = novels()
    novel.id = results[0]
    novel.title = results[1]
    novel.img = results[2]
    novel.author = results[3]
    novel.genre = results[4]
    novel.link = results[5]
    description = results[6].replace('\n','<br>')
    novel.chapter = results[7]
    mycursor.execute(f"select chapterno,chapter_title,chapter_link from chapters where novelID = {novel.id};")
    chapterss = mycursor.fetchall()
    chapters = []
    for chap in chapterss:
        c = chapter()
        c.no = chap[0]
        c.title = chap[1]
        c.link = chap[2]
        chapters.append(c)
    return render(request,'details.html',{'novel':novel,'chapters':chapters,'description':description})

def search(request):
    mydb = mysql.connector.connect(
    host="localhost",
    user="bhumit",
    password="admin123",
    database="novels"
    )
    searchterms = ''
    title = request.GET['term']
    genre = request.GET['genre']
    author = request.GET['author']
    if title == '':
        if genre == '':
            if author == '':
                query = "select novelID,title,image,author,genre,url from novelsdetails limit 40;"
            else:
                query = f"select novelID,title,image,author,genre,url from novelsdetails where author like '%{author}%' limit 40;"
        else:
            if author == '':
                query = f"select novelID,title,image,author,genre,url from novelsdetails where genre like '%{genre}%' limit 40;"
            else:
                query = f"select novelID,title,image,author,genre,url from novelsdetails where author like '%{author}%' and genre like '%{genre}%' limit 40;"
    else:
        if genre == '':
            if author == '':
                query = f"select novelID,title,image,author,genre,url from novelsdetails where title like '%{title}%' limit 40;"
            else:
                query = f"select novelID,title,image,author,genre,url from novelsdetails where author like '%{author}%' and title like '%{title}%' limit 40;"
        else:
            if author == '':
                query = f"select novelID,title,image,author,genre,url from novelsdetails where title like '%{title}%' and genre like '%{genre}%' limit 40;"
            else:
                query = f"select novelID,title,image,author,genre,url from novelsdetails where author like '%{author}%' and genre like '%{genre}%' and title like '%{title}%' limit 40;"
    mycursor = mydb.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    novelss = []
    for results in myresult:
        novel = novels()
        novel.id = results[0]
        novel.title = results[1]
        novel.img = results[2]
        novel.author = results[3]
        novel.genre = results[4]
        novel.link = results[5]
        novelss.append(novel)
    return render(request,'home.html',{'novels':novelss})

def genre(request):
    mydb = mysql.connector.connect(
    host="localhost",
    user="bhumit",
    password="admin123",
    database="novels"
    )
    searchterm = request.GET['genre']
    mycursor = mydb.cursor()
    mycursor.execute("select novelID,title,image,author,genre,url from novelsdetails where genre like '%"+ searchterm+ "%'  limit 40;")
    myresult = mycursor.fetchall()
    novelss = []
    for results in myresult:
        novel = novels()
        novel.id = results[0]
        novel.title = results[1]
        novel.img = results[2]
        novel.author = results[3]
        novel.genre = results[4]
        novel.link = results[5]
        novelss.append(novel)
    return render(request,'home.html',{'novels':novelss})
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="bhumit",
  password="admin123",
  database="novels"
)

def create_novelsdetails(novelID,title,url,chapters,author,genre,about,img):
    global mydb
    mycursor = mydb.cursor()
    sql = "INSERT INTO novelsdetails (novelID,title, url, author, chapters, description, image, genre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (novelID,title,url,author,chapters,about,img,genre)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


def create_chapters(data): #data is arguments in form of list of tuples
    global mydb
    mycursor = mydb.cursor()
    sql = "INSERT INTO chapters(novelID,chapterno,chapter_title,chapter_link) VALUES (%s,%s,%s,%s)"
    mycursor.executemany(sql, data)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


def create_novels(title,url):
    global mydb
    mycursor = mydb.cursor()
    sql = "INSERT INTO test (title, url) VALUES (%s, %s)"
    val = (title,url)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

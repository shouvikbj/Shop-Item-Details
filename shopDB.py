import sqlite3

con = sqlite3.connect('shopDetails.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS shop(
            shopname VARCHAR2(2000),
            owner VARCHAR2(500),
            email VARCHAR2(500),
            address VARCHAR2(1000000),
            password VARCHAR2(500),
            image VARCHAR2(1000)
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS shopBackUp AS SELECT * FROM shop WHERE 1=1;
    """)

def shopLogin(email):
    db.execute("SELECT email,password FROM shop WHERE email = (?)",(email,))
    shop = db.fetchall()
    return shop

def createShop(shopname,owner,email,address,password,img):
    db.execute("INSERT INTO shop VALUES(?,?,?,?,?,?)",(shopname,owner,email,address,password,img))
    db.execute("INSERT INTO shopBackUp VALUES(?,?,?,?,?,?)",(shopname,owner,email,address,password,img))
    con.commit()

def getShop(email):
    db.execute("SELECT * FROM shop WHERE email = (?)",(email,))
    shop = db.fetchall()
    return shop

def updateInfo(shopname,owner,email,address,password,img):
    db.execute("UPDATE shop SET shopname=(?),owner=(?),address=(?),password=(?),image=(?) WHERE email=(?)",(shopname,owner,address,password,img,email))
    db.execute("INSERT INTO shopBackUp VALUES(?,?,?,?,?,?)",(shopname,owner,email,address,password,img))
    con.commit()

def getImage(email):
    db.execute("SELECT image FROM shop WHERE email=(?)",(email,))
    image = db.fetchall()
    return image[0][0]

def getPassword(email):
    db.execute("SELECT password FROM shop WHERE email=(?)",(email,))
    password = db.fetchall()
    return password[0][0]



#createTable()
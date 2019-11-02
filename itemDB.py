import sqlite3

con = sqlite3.connect('items.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR2(10000),
            itemname VARCHAR2(5000),
            itemdesc VARCHAR2(10000000000),
            units VARCHAR2(500),
            mrp VARCHAR2(500),
            awaycost VARCHAR2(500),
            awaypktcost VARCHAR2(500),
            localcost VARCHAR2(500),
            localpktcost VARCHAR2(500),
            date VARCHAR2(100),
            img VARCHAR2(1000)
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS itemsBackUp AS SELECT * FROM items WHERE 1=1;
    """)

def enterItem(email,itemname,itemdesc,units,mrp,awaycost,awaypktcost,localcost,localpktcost,date,img):
    db.execute("INSERT INTO items VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?)",(email,itemname,itemdesc,units,mrp,awaycost,awaypktcost,localcost,localpktcost,date,img))
    db.execute("INSERT INTO itemsBackUp VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?)",(email,itemname,itemdesc,units,mrp,awaycost,awaypktcost,localcost,localpktcost,date,img))
    con.commit()

def getItems(email):
    db.execute("SELECT * FROM items WHERE email=(?)",(email,))
    items = db.fetchall()
    return items

def getItem(email,pid):
    db.execute("SELECT * FROM items WHERE (email=(?) AND id=(?))",(email,pid))
    item = db.fetchall()
    return item

def getImage(pid):
    db.execute("SELECT img FROM items WHERE id=(?)",(pid,))
    image = db.fetchall()
    return image[0][0]

def updateItem(email,itemname,itemdesc,units,mrp,awaycost,awaypktcost,localcost,localpktcost,date,img,pid):
    db.execute("UPDATE items SET email=(?),itemname=(?),itemdesc=(?),units=(?),mrp=(?),awaycost=(?),awaypktcost=(?),localcost=(?),localpktcost=(?),date=(?),img=(?) WHERE id=(?)",(email,itemname,itemdesc,units,mrp,awaycost,awaypktcost,localcost,localpktcost,date,img,pid))
    db.execute("INSERT INTO itemsBackUp VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?)",(email,itemname,itemdesc,units,mrp,awaycost,awaypktcost,localcost,localpktcost,date,img))
    con.commit()




#createTable()
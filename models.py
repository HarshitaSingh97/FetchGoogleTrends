
import sqlite3 as sql
import os.path

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#db_path = os.path.join(BASE_DIR,"database.db")
datafile =  "database.db"
datadir = '//var//www//html//flaskapp//'
#datadir = '../flaskapp/'
db = datadir+datafile
def checkUser(username):
    con = sql.connect(db)
    cur = con.cursor()
    try:
        cur.execute("SELECT username FROM users")
        users = cur.fetchall()
        username=(username,)
        if(username in users):
            return 1
        else:
            return 0
        return 1
    except:
	return 0
    finally:
	con.commit()
        con.close()

def insertUser(username,password):
    con = sql.connect(db)
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def retrieveUsers():
        con = sql.connect(db)
        cur = con.cursor()
        cur.execute("SELECT username, password FROM users")
        users = cur.fetchall()
        con.close()
        return users

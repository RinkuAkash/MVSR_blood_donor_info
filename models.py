import sqlite3 as sql

def retrieveAdmin():
    con = sql.connect("database.db")
    cur =con.cursor()
    cur.execute("SELECT username, password FROM admin")
    users = cur.fetchall()
    con.close()
    return users
import sqlite3
from sys import path
from uuid import uuid4

path.append("..")

from connection import connection, cursor

cursor.execute("CREATE TABLE IF NOT EXISTS session_uuids (username TEXT NOT NULL, uuid TEXT NOT NULL, expiry INTEGER NOT NULL, hash TEXT NOT NULL, PRIMARY KEY (uuid))")

def create(username, expiry, hash): #Oturum açmayı sağlayan fonksiyon.
    try:
        uuid = None
        while uuid == cursor.execute("SELECT uuid FROM session_uuids WHERE username = ?", (username,)).fetchone()[0]:
            uuid = uuid4().hex

        cursor.execute("INSERT INTO session_uuids VALUES (?, ?, ?)", (username, uuid, expiry, hash))
    except sqlite3.OperationalError:
        raise Exception("couldntinsert")
    else:
        connection.commit()
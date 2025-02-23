import sqlite3
from sys import path
from uuid import uuid4

path.append("..")

import utilities.validation as validation
from database.connection import connection, cursor

cursor.execute("CREATE TABLE IF NOT EXISTS session_uuids (username TEXT NOT NULL, uuid TEXT NOT NULL, expiry INTEGER NOT NULL, hash TEXT NOT NULL, PRIMARY KEY (uuid))")

def create(username, expiry, hash):
    try:
        uuid = None
        while uuid == cursor.execute("SELECT uuid FROM session_uuids WHERE username = ?", (username,)).fetchone()[0]:
            uuid = uuid4().hex

        cursor.execute("INSERT INTO session_uuids VALUES (?, ?, ?)", (username, uuid, expiry, hash))
    except sqlite3.OperationalError:
        raise Exception("couldntinsert")
    else:
        connection.commit()

def check(uuid): #İndis numarası eklemeyi unutma!
    try:
        data = cursor.execute("SELECT expiry, username FROM session_uuids WHERE uuid = ?", (uuid,)).fetchone()
    except sqlite3.OperationalError:
        return False, None
    else:
        return validation.timestamp(data[0]), data[1]

def owner(uuid):
    try:
        owner = cursor.execute("SELECT username FROM session_uuids WHERE uuid = ?", (uuid,)).fetchone()[0]
    except sqlite3.OperationalError:
        raise Exception("nosessionuuid")
    else:
        return owner

def get_hash(uuid):
    try:
        hash = cursor.execute("SELECT hash FROM session_uuids WHERE uuid = ?", (uuid,)).fetchone()[0]
    except sqlite3.OperationalError:
        raise Exception("nosessionuuid")
    else:
        return hash
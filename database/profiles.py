import sqlite3
from sys import path

path.append("..")

import utilities.generation as generation
from connection import connection, cursor

cursor.execute("CREATE TABLE IF NOT EXISTS profiles (username TEXT NOT NULL, expiration INTEGER NOT NULL, PRIMARY KEY (username))")
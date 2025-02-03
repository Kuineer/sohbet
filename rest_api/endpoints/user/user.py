import sqlite3

import utilities.generation as generation
from database.connection import cursor
from rest_api.presets import nouser, usepost

class endpoint:
    def __init__(self, arguments, controls, queries):
        self.arguments = arguments
        self.controls = controls
        self.queries = queries

    config = {
        "arguments": {
            "required": ("username", "session_uuid"),
            "optional": ((),)
        },
        "controls": {
            "fetch_from_db": {
                "query": True,
                "table": "users", #Doğrudan tablo adı
                "row": "username", #Doğrudan satır adı
                "where": "username" #Argüman adı
            },
            "is_session_user_requested": {
                "query": True,
                "username": "username",
                "uuid": "session_uuid"
            },
            "session_expired": {
                "query": False
            }
        }
    }

    def get(self):
        return usepost

    def post(self):
        try:
            data = cursor.execute("SELECT * FROM users WHERE username = ?", (self.arguments["username"],)).fetchone()[0]
        except sqlite3.OperationalError:
            return nouser

        username = self.arguments["username"]
        if self.queries[1]:

            return {
                "success": True,
                "data": {
                    "public": {
                        "username": username,
                        "toc": data[1],
                        "biography": data[7]
                    },
                    "private": {
                        "settings": generation.aes_decrypt(data[3], hash),
                        "group_settings": generation.aes_decrypt(data[4], hash)
                    }
                },
            }
        else:
            return {
                "success": True,
                "data": {
                    "public": {
                        "username": username,
                        "toc": data[1],
                        "biography": data[7]
                    }
                }
            }
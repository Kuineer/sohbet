import sqlite3

import database.rooms as rooms
from rest_api.presets import nouser, success, usepost

class endpoint:
    def __init__(self, arguments, controls, queries):
        self.arguments = arguments
        self.controls = controls
        self.queries = queries

    config = {
        "arguments": ("uuid", "private_key", "administrator_hash"),
        "controls": {
            "asd_permission": {
                "query": True,
                "type": "type",
                "private_key": "private_key",
                "administrator_hash": "administrator_hash",
                "username": "username",
                "uuid": "uuid"
            }
        }
    }

    def get(self):
        return usepost

    def post(self):
        try:
            rooms.delete(self.arguments["uuid"])
        except sqlite3.OperationalError:
            return nouser
        except Exception as code:
            return {
                "success": False,
                "error": code
            }
        else:
            return success
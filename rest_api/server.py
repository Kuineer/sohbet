#Production mode için: https://flask.palletsprojects.com/en/stable/deploying/
import sqlite3
from flask import Flask
from flask_restful import Api, Resource, reqparse

import database.users as users
import utilities.validation as validation
from database.connection import cursor
from database.rooms import has_permissions
from presets import *

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument(
    "biography",
    "channel_settings",
    "expiry",
    "message",
    "password",
    "permission_map"
    "recipient",
    "room_settings",
    "sender",
    "session_uuid",
    "settings",
    "title",
    "type",
    "username",
)

import endpoints

map = { #Tüm endpoint isimleri karşılık geldikleri classlara eşleştirilecek.
    "channel": {
        "channel": endpoints.channel.channel.endpoint
    },
    "friend_request": {
        "friend_request": endpoints.friend_request.friend_request.endpoint,
        "accept": endpoints.friend_request.accept.endpoint,
        "cancel": endpoints.friend_request.cancel.endpoint,
        "decline": endpoints.friend_request.decline.endpoint,
        "send": endpoints.friend_request.send.endpoint
    },
    "message": {

    },
    "room": {
        "room": endpoints.room.room.endpoint,
        "create": endpoints.room.create.endpoint,
        "create_channel": endpoints.room.create_channel.endpoint,
        "delete": endpoints.room.delete.endpoint,
        "join": endpoints.room.join.endpoint,
        "updadte": endpoints.room.update.endpoint
    },
    "room_invite": {

    },
    "session": {
        "session": endpoints.session.session.endpoint,
        "new": endpoints.session.new.endpoint,
        "terminate": endpoints.session.terminate.endpoint
    },
    "status": {
        "status": endpoints.status.status.endpoint,
        "past_announcements": endpoints.status.past_announcements.endpoint,
        "time": endpoints.status.time
    },
    "user": {
        "user": endpoints.user.user.endpoint,
        "create": endpoints.user.create.endpoint,
        "delete": endpoints.user.delete.endpoint,
        "update": endpoints.user.update.endpoint
    }
}

def endpoint(endpoint):
    arguments = parser.parse_args()
    if not endpoint.config["arguments"] in arguments:
        return missingarguments

    controls = endpoint.config["controls"]
    queries = []

    access_to_channel = controls["access_to_channel"]
    access_to_room = controls["access_to_room"]
    asd_permission = controls["asd_permission"]
    check_booleans = controls["check_booleans"]
    fetch_from_db = controls["fetch_from_db"]
    has_permission = controls["fetch_from_db"]
    is_integer = controls["is_integer"]
    is_uuid = controls["is_uuid"]
    username_taken = controls["username_taken"]
    user_exists = controls["user_exists"]
    if access_to_channel:
        pass #Veri tabanından permissions alınacak ve şifresi çözülecek, o veri okunarak karar verilecek.
    if access_to_room:
        pass #
    if asd_permission: #asd: access to sensitive data
        pass #
    if check_booleans: #List çıktı
        result = []
        for argument in check_booleans:
            result.append(argument is None)
        if check_booleans["query"]: queries.append(result)
        elif not all(result): return notallofthemaretrue
    if fetch_from_db:
        try:
            cursor.execute("SELECT * FROM ? WHERE ? = ?", (fetch_from_db["table"], fetch_from_db["row"], arguments[fetch_from_db["where"]]))
        except sqlite3.OperationalError:
            result = False
        else:
            result = True
        if fetch_from_db["query"]: queries.append(result)
        elif not result: return nouser
    if has_permission:
        result = has_permissions(has_permission["uuid"], has_permission["username"], has_permission["permission"], arguments[has_permission["administrator_hash"]])
        if has_permission["query"]: queries.append(result)
        elif not result: return nopermission
    if is_integer:
        result = validation.integer(arguments[is_integer["argument"]])
        if is_integer["query"]: queries.append(result)
        elif not result: return invalidformat
    if is_uuid:
        result = validation.uuid(arguments[is_uuid["uuid"]], is_uuid["version"])
        if is_uuid["query"]: queries.append(result)
        elif not result: return invalidformat
    if username_taken:
        for user in username_taken["usernames"]:
            result = users.exists(user)
            if username_taken["query"]: queries.append(result)
            elif not result: return nouser
    if user_exists:
        for user in user_exists["users"]:
            result = users.exists(user)
            if user_exists["query"]: queries.append(result)
            elif not result: return nouser

    return endpoint(Resource, arguments, queries)

#Bu alanda birçok errorhandler bulunacak.

@app.errorhandler(404)
def error_404(error):
    return {
        "success": False,
        "error": "notfound",
    }, 404

#API'ye eklemeler burada olacak.
#API eklemeleri gerçekleşince ve sunucu başlatılınca log edilecek.
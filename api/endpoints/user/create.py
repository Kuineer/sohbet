from flask import request

import api.controls as controls
import api.presets as presets
import database.users as users
from api.app import api

@api.route("/user/create", methods=["GET", "POST"])
@api.route("/user/create/", methods=["GET", "POST"])
def user_create():
    parameters = request.args if request.method == "GET" else request.form

    if controls.check_parameters(parameters, ("username", "password")):
        username = parameters["username"]
        password = parameters["password"]

        if controls.user_exists(username): return presets.userexists
    else:
        return presets.missingparameter

    if not (
        3 <= len(username) <= 36 and
        18 <= len(password) <= 45 and
        all(character not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.;-_!?'\"#%&/\()[]{}=" for character in password)
    ): return presets.invalidusername
    if not password.isascii(): return presets.invalidformat

    try:
        hash, salt = users.create(username, password)
    except Exception as code:
        return {
                "success": False,
                "error": code
            }, presets.status_codes[code]

    return {
            "success": True,
            "user": {
                "username": username,
                "hash": hash,
                "salt": salt
            }
        }, 201

def reference():
    pass #(...)
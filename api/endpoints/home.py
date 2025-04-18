from api.app import api

@api.route("/", methods=["GET", "POST"])
def home():
    return {
        "success": True,
        "endpoints": {
            "home": "/",
            "reference": "/reference",
            "channel": {
                "channel": "/channel",
                "create": "/channel/create",
                "update_permissions": "/room/update_permissions"
            },
            "conversation": {
                "conversation": "/conversation",
                "create": "/conversation/create",
                "delete": "/conversation/delete"
            },
            "message": {
                "message": "/message",
                "create": "/message/create",
                "delete": "/message/delete",
                "edit": "/message/edit"
            },
            "request": {
                "request": "/request",
                "accept": "/request/accept",
                "decline": "/request/decline",
                "withdraw": "/request/withdraw"
            },
            "room": {
                "room": "/room",
                "create": "/room/create",
                "delete": "/room/delete",
                "update": "/room/update",

                "member": "/member",
                "kick": "/member/kick"
            },
            "user": {
                "user": "/user",
                "create": "/user/create",
                "delete": "/user/delete",
                "update": "/user/update"
            }
        }
    }, 200
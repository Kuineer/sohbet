#[7203, 7214] aralığındaki portlar bilinen başka hizmetler tarafından kullanılmıyor.
app_name = "Sohbet"

class UserConnection:
    host = "0.0.0.0"
    port = 7204
user_connection = UserConnection()

class Database:
    file_name = "database"
    default_user_settings = "" #Henüz hazır değil. Virgülle ayrılacak.
    default_channel_pm = ""
    default_group_pm = ""
database = Database()

class Room:
    #Farklı type değerleri için farklı varsayılanlar
    default_settings_0 = """
{
    "member_limit": 10
}
"""
    default_settings_1 = """

"""
    default_pm = """
"members": {
    "{}": {
        "icon": null,
        "color": "666699",
        "permissions": {
            "all": true
        }
    }
}
"""
room = Room()

class Message:
    character_limit = 4000
message = Message()

class RESTAPI:
    host = "0.0.0.0"
    port = 7203
    path = "/api"
    incidents_path = "incident"
rest_api = RESTAPI()
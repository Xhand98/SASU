    import threading
import time
import sqlite3
from NewSimpleSQL.SimpleSQLite import Database


def update_user_info():
       connection = sqlite3.connect("./db/users.db")
       db = Database(connection)
       users = db.complicated_select_data([
           {
            "name" : "steam_accounts",
            "columns": "steam_id, discord_user_id",
            "conditions" : f"",
            "fetch" : True
           },
           {
           "name" : "discord_users",
           "columns" : "discord_id, discord_username",
           "conditions" : f"",
           "fetch" : True
           }])
       print(users)
       db.close()


update_thread = threading.Thread(target=update_user_info)

update_thread.start()

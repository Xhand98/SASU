import threading
import time
import sqlite3
from NewSimpleSQL import Database


def update_user_info():
    while True:
        connection = sqlite3.connect("steam_user.db")
        db = Database(connection)

        users = db.simple_select_data("users", "*")

        for user in users:
            discord_id, steam_id = user

            print(f"actualizando informacion para el steam id: {steam_id}")

        db.close()
        time.sleep(30)


update_thread = threading.Thread(target=update_user_info)

update_thread.start()

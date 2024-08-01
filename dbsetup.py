import sqlite3
from NewSimpleSQL import Database

connection = sqlite3.connect('steam_users.db')
db = Database(connection)

structure = {
    "name": "users",
    "columns": [
        {"name": "discord_id", "type":"TEXT"},
        {"name": "steam_id", "type":"TEXT"}
    ]
}

db.simple_create_table(structure)

db.close()
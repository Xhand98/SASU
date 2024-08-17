import os
import sqlite3
from NewSimpleSQL import Database


folderName = 'db'
fileName = 'sasu_users.db'

db_path =os.path.join('db', 'sasu_users.db')
if not os.path.exists(folderName):
    os.makedirs(folderName)

connection = sqlite3.connect('./db/sasu_users.db')
db = Database(connection)

structure1 = {
    "name": "discord_users",
    "columns": [
        {"name": "id", "type": "INTEGER PRIMARY KEY AUTOINCREMENT"},
        {"name": "discord_id", "type": "TEXT"},
        {"name": "discord_username", "type": "TEXT"},
        {"name": "created_at", "type": "TEXT"},  # Use TEXT for datetime
        {"name": "updated_at", "type": "TEXT"}
    ]
}

structure2 = {
    "name": "steam_accounts",
    "columns": [
        {"name": "id", "type": "INTEGER PRIMARY KEY AUTOINCREMENT"},
        {"name": "discord_user_id", "type": "INTEGER"},
        {"name": "steam_id", "type": "TEXT"},
        {"name": "steam_username", "type": "TEXT"},
        {"name": "created_at", "type": "TEXT"},
        {"name": "updated_at", "type": "TEXT"}
    ]
}

db.simple_create_table(structure1)
db.simple_create_table(structure2)

db.close()
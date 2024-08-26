import os
import sqlite3
from NewSimpleSQL import Database


connection = sqlite3.connect('./example.db')
db = Database(connection)

structure1 = {
    "name": "discord_users",
    "columns": [
        {"name": "id", "type": "INTEGER PRIMARY KEY AUTOINCREMENT"},
        {"name": "discord_id", "type": "TEXT"},
        {"name": "discord_username", "type": "TEXT"},
        {"name": "created_at", "type": "TEXT"},  
        {"name": "updated_at", "type": "TEXT"}
    ]
}

structure2 = {
    "name": "steam_accounts",
    "columns": [
        {"name": "id", "type": "INTEGER PRIMARY KEY AUTOINCREMENT"},
        {"name": "steam_id", "type": "TEXT"},
        {"name": "steam_username", "type": "TEXT"},
        {"name": "created_at", "type": "TEXT"},
        {"name": "updated_at", "type": "TEXT"}
    ]
}

db.simple_create_table(structure1)
db.simple_create_table(structure2)

db.close()

print("Your database has been set up. :D")
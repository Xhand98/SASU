import os
import sqlite3
from NewSimpleSQL.SimpleSQLite import Database, ID


connection = sqlite3.connect("./db/users.db")
db = Database(connection)

structure1 = {
    "name": "discord_users",
    "columns": {
        "discord_id": ID(auto_increment=False),
        "discord_username": {"type": str, "constraints": "NOT NULL"},
        "created_at": str,
        "updated_at": str,
    },
}
structure2 = {
    "name": "steam_accounts",
    "columns": {
        "steam_id": ID(auto_increment=False),
        "discord_user_id": {"type": int, "constraints": "NOT NULL"},
        "steam_username": {"type": str, "constraints": "NOT NULL"},
        "created_at": str,
        "updated_at": str,
    },
    "fk": {"discord_user_id": ("discord_users", "discord_id", True)},
}
structure3 = {
    "name": "blacklist",
    "columns": {
                "discord_id": ID(auto_increment=False),
                "banned_at": str,
                },
    "fk": {"discord_id": ("discord_users", "discord_id")},
}

db.complicated_create_tables([structure1, structure2, structure3])
db.close()

print("Your database has been set up. :D")

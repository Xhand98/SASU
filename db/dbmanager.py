import sqlite3
from NewSimpleSQL.SimpleSQLite import Database, ID
import datetime


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.db = Database(self.conn)

    def close(self):
        self.db.close()

    def get_discord(self):
        self.db.simple_select_data("discord_users", "*")

    def create_tables(self):
        structure1 = {
            "name": "discord_users",
            "columns": {
                "id": ID(),
                "discord_id": {"type": str, "constraints": "NOT NULL"},
                "discord_username": {"type": str, "constraints": "NOT NULL"},
                "created_at": str,
                "updated_at": str,
            },
        }
        structure2 = {
            "name": "steam_accounts",
            "columns": {
                "id": ID(),
                "discord_user_id": {"type": int, "constraints": "NOT NULL"},
                "steam_id": {"type": int, "constraints": "NOT NULL"},
                "steam_username": {"type": str, "constraints": "NOT NULL"},
                "created_at": str,
                "updated_at": str,
            },
            "fk": [
                {
                    "column": "discord_user_id",
                    "references": ["discord_users", "discord_id"],
                }
            ],
        }
        structure3 = {
            "name": "blacklist",
            "columns": {
                "id": ID(),
                "discord_id": {"type": str, "constraints": "NOT NULL"},
            },
            "fk": [
                {"column": "discord_id", "references": ["discord_users", "discord_id"]}
            ],
        }

        self.db.complicated_create_tables([structure1, structure2, structure3])

    def link_steam_id(
        self, discord_id: int, steam_id: int, steam_username: str, discord_username: str
    ):
        # Insert data into steam_accounts table
        self.db.simple_insert_data(
            "steam_accounts",
            (
                steam_id,
                discord_id,
                steam_username,
                str(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ),  # created_at
                str(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ),  # updated_at
            ),
        )

        # Insert data into discord_users table
        self.db.simple_insert_data(
            "discord_users",
            (
                discord_id,
                discord_username,
                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ),
        )

    def get_steam_info(self, discord_id):
        tables = [
            {
                "name": "steam_accounts",
                "columns": "*",
                "conditions": f"WHERE discord_user_id = '{discord_id}'",
                "fetch": True,
            },
            {
                "name": "discord_users",
                "columns": "*",
                "conditions": f"WHERE discord_id = '{discord_id}'",
                "fetch": True,
            },
        ]

        data = self.db.complicated_select_data(tables)

        return data

    def ban(self, discord_id: int):
        self.db.simple_insert_data(
            "blacklist",
            (
                discord_id,
                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            ),
        )

    def isbanned(self, discord_id: int):
        if self.db.simple_select_data(
            "blacklist", "discord_id", f"WHERE discord_id = '{discord_id}'"
        ):
            return True
        else:
            return False

    def unban(self, discord_id):
        self.db.simple_delete_data("blacklist", f"discord_id = '{discord_id}'")
        return "User is now unbanned"

    def run_custom_query(self, query):
        self.db.custom_execute(query)

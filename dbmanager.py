import sqlite3
from NewSimpleSQL import Database
import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.db = Database(self.conn)
    
    def close(self):
        self.db.close()

    def create_tables(self):
        table_structure1 = {
            "name": "discord_users",
            "columns": [
                {"name": "id", "type": "INTEGER PRIMARY KEY AUTOINCREMENT"},
                {"name": "discord_id", "type": "TEXT"},
                {"name": "discord_username", "type": "TEXT"},
                {"name": "created_at", "type": "TEXT"},  # Use TEXT for datetime
                {"name": "updated_at", "type": "TEXT"}
       ]
    }

        table_structure2 = {
        "name": "steam_accounts",
        "columns": [
            {"name": "id", "type": "INTEGER PRIMARY KEY AUTOINCREMENT"},
            {"name": "discord_user_id", "type": "TEXT"},
            {"name": "steam_id", "type": "TEXT"},
            {"name": "steam_username", "type": "TEXT"},
            {"name": "created_at", "type": "TEXT"},
            {"name": "updated_at", "type": "TEXT"}
        ]
    }
        self.db.simple_create_table(table_structure1)
        self.db.simple_create_table(table_structure2)

    def link_steam_id(self, discord_id: int, steam_id: str, steam_username: str, discord_username: str):
    # Insert data into steam_accounts table
        self.db.simple_insert_data(
            "steam_accounts", 
            (
                None,  
                discord_id,
                steam_id,
                steam_username,
                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  # created_at
                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))   # updated_at
            )
        )

        # Insert data into discord_users table
        self.db.simple_insert_data(
            "discord_users",
            (
                None,
                discord_id,
                discord_username,
                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  
                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))   
            )
        )
    def get_steam_info(self, discord_id):
        tables = [
            {
                "name": "steam_accounts",
                "columns": "*",
                "conditions": f"WHERE discord_user_id = '{discord_id}'",
                "fetch": True
            },
            {
                "name": "discord_users",
                "columns": "*",
                "conditions": f"WHERE discord_id = '{discord_id}'",
                "fetch": True
            }
        ]

        data = self.db.complicated_select_data(tables)

        return data
        ## "users", "steam_id", f"WHERE discord_id = '{discord_id}'", one_fetch=True

    def update_steam_info(self):
        # Placeholder para lógica de actualización periódica
        users = self.db.simple_select_data("users", "*")
        for user in users:
            discord_id, steam_id = user
            print(f"Actualizando información para Steam ID: {steam_id}")
    
    def run_custom_query(self, query):
        self.db.custom_execute(query)



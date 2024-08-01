import sqlite3
from NewSimpleSQL import Database

class DatabaseManager:
    def __init__(self, db_path='steam_users.db'):
        self.db_path = db_path

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.db = Database(self.conn)
    
    def close(self):
        self.db.close()

    def create_table(self):
        table_structure = {
            "name": "users",
            "columns": [
                {"name": "discord_id", "type": "TEXT"},
                {"name": "steam_id", "type": "TEXT"}
            ]
        }
        self.db.simple_create_table(table_structure)

    def link_steam_id(self, discord_id, steam_id):
        self.db.simple_insert_data("users", (discord_id, steam_id))

    def get_steam_id(self, discord_id):
        return self.db.simple_select_data("users", "steam_id", f"WHERE discord_id = '{discord_id}'", one_fetch=True)

    def update_steam_info(self):
        # Placeholder para lógica de actualización periódica
        users = self.db.simple_select_data("users", "*")
        for user in users:
            discord_id, steam_id = user
            print(f"Actualizando información para Steam ID: {steam_id}")
    
    def run_custom_query(self, query):
        self.db.custom_execute(query)



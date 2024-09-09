# db_operations.py
import os
import shutil
from datetime import datetime
from db.dbmanager import DatabaseManager as Dbm


class DatabaseOperations:
    def __init__(self, db_path):
        self.db_path = db_path

    async def get_steamid_from_db(self, discord_id: str):
        db = Dbm(db_path=self.db_path)
        db.connect()
        data = db.get_steam_info(discord_id)
        db.close()
        return data

    async def is_banned(self, discord_id):
        db = Dbm(db_path=self.db_path)
        db.connect()
        queso = db.isbanned(discord_id)
        db.close()
        return queso

    async def ban_user(self, discord_id):
        db = Dbm(db_path=self.db_path)
        db.connect()
        db.ban(discord_id)
        db.close()

    async def unban_user(self, discord_id):
        db = Dbm(db_path=self.db_path)
        db.connect()
        db.unban(discord_id)
        db.close()

    def backup_database(self):
        """
        Creates a backup of the database file in the ./db/backup directory.

        The filename of the backup is in the format "YYYYMMDD_HHMMSS_backup.db",
        where the timestamp is the current local time when this function is called.
        """
        file = self.db_path
        time = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = "./db/backup"
        changed_name = os.path.join(backup_dir, f"{time}_backup.db")
        shutil.copy(file, changed_name)
        print(f"Backup created: {changed_name}")

    # Add other database-related methods here

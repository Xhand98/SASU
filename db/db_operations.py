# db_operations.py
import os
import shutil
from datetime import datetime
from db.dbmanager import DatabaseManager as Dbm


class DatabaseOperations:
    """
    A class to manage database operations for the bot.

    Attributes
    ----------
    self.db_path : str
        The path to the database file.

    Methods
    -------
    get_steamid_from_db(self, discord_id: str)
        Retrieves Steam account information for
        a Discord user.
    """

    def __init__(self):
        """
        Initializes a DatabaseOperations object.

        Parameters
        ----------
        db_path : str
            The path to the database file.

        Attributes
        ----------
        self.db_path : str
            The path to the database file.
        """
        # self.db_path = db_path

    async def get_steamid_from_db(self, discord_id: str):
        """
        Retrieves Steam account information for
        a Discord user.

        Parameters
        ----------
        discord_id : str
            The Discord ID of the user to
            retrieve information for

        Returns
        -------
        list
            A list of dictionaries containing
            the user's Steam account info
        """
        
        db = Dbm()
        
        return db.get_steam_info(discord_id).steam_id

    async def is_banned(self, discord_id):
        """
        Checks if a Discord user is banned from using the bot

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user to check

        Returns
        -------
        bool
            True if the user is banned, False otherwise
        """
        
        return Dbm.isbanned(discord_id)

    async def ban_user(self, discord_id):
        """
        Bans a Discord user from using the bot

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user to ban

        Returns
        -------
        None

        Raises
        ------
        Exception
            If an error occurs during the ban.
        """
        db = Dbm()
        return db.ban(discord_id)

    async def unban_user(self, discord_id):
        """
        Unbans a Discord user from using the bot

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user to unban

        Returns
        -------
        None

        Raises
        ------
        Exception
            If an error occurs during the unban.
        """
        db = Dbm()
        db.unban(discord_id)

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

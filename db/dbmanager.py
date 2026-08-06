# import sqlite3
from db.models import DiscordUser, SteamAccount, Blacklist
from NewSimpleSQL.SimpleSQLite import Database, ID
from datetime import datetime

class DatabaseManager:
    """
    A class to manage database operations for the bot.
    Attributes:
        self.db_path (str): The path to the database file.
        self.conn (sqlite3.Connection): The SQLite connection object.
        self.db (NewSimpleSQL.SimpleSQLite.Database): The database object.
    Methods:
        connect(): Establishes a connection to the database.
        close(): Closes the database connection.
        get_discord(): Retrieves Discord user data.
        create_tables(): Creates necessary tables in the database.
        link_steam_id(discord_id, steam_id, steam_username, discord_username):
        Links a Steam account to a Discord user.
        get_steam_info(discord_id): Retrieves Steam account
        information for a Discord user.
        ban(discord_id): Bans a Discord user.
        isbanned(discord_id): Checks if a Discord user is banned.
        unban(discord_id): Unbans a Discord user.
        run_custom_query(query): Executes a custom SQL query.
        update_user_info(discord_id, new_username, date):
        Updates user information.
        backup_database(): Creates a backup of the database.
    """

    def __init__(self):
        """
        Initializes a DatabaseManager object.
        """

    def get_discord(self):
        """
        Retrieves Discord user data.

        Returns
        -------
        list
            A list of tuples containing the Discord ID, username, created_at, and
            updated_at for each user in the database.
        """
        # self.db.simple_select_data("discord_users", "*")
        DiscordUser.select()

    def link_steam_id(
        self, discord_id: str, steam_id: str, steam_username: str, discord_username: str
    ):
        """
        Links a Steam account to a Discord user.

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user to link.
        steam_id : int
            The Steam ID of the account to link.
        steam_username : str
            The username of the Steam account to link.
        discord_username : str
            The username of the Discord user to link.
        """
        
        user, _ = DiscordUser.get_or_create(
            discord_id = discord_id,
            defaults={
                'username': discord_username,
            },
        )
        SteamAccount.get_or_create(
            discord=user,
            defaults={
                'steam_id': steam_id,
                'username': steam_username
            },
        )

    def get_steam_info(self, discord_id):
        """
        Retrieves Steam account information for a Discord user.

        Parameters
        ----------
        discord_id : str
            The Discord ID of the user to retrieve information for

        Returns
        -------
        list
            A list of dictionaries containing the user's Steam account info
        """
        user = DiscordUser.get_or_none(
            DiscordUser.discord_id == discord_id
        )
        
        if user is None:
            return None
        
        return SteamAccount.get_or_none(
            SteamAccount.discord == user
        )

    def ban(self, discord_id: int):
        """
        Bans a Discord user from using the bot

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user to ban
            
        Returns
        ----------
        bool
            True if the user got banned, False if not
        """
        user = DiscordUser.get_or_none(
            DiscordUser.discord_id == discord_id
        )
        
        if user is None:
            return False
        
        _, created = Blacklist.get_or_create(
            discord = user,
        )
        
        return created

    def isbanned(self, discord_id: int):
        """
        Checks if a Discord user is banned from using the bot

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user

        Returns
        -------
        bool
            True if the user is banned, False otherwise
        """
        user = DiscordUser.get_or_none(
            DiscordUser.discord_id == discord_id
        )
        
        if user is None:
            return False
        
        return Blacklist.get_or_none(
            Blacklist.discord == user
        ) is not None

    def unban(self, discord_id):
        """
        Unbans a Discord user from using the bot.

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user to unban.

        Returns
        -------
        str
            A success message if the user is unbanned successfully.
        """
        
        user = DiscordUser.get_or_none(
            DiscordUser.discord_id == discord_id
        )
        
        if user is None:
            return False
        
        return (
            Blacklist
            .delete()
            .where(user.discord_id == discord_id)
            .execute()) > 0

    def update_user_info(self, discord_id, new_username, date):
        """
        Updates user information in the database.

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user to update.
        new_username : str
            The new username of the user.
        date : str
            The date to update the user's information (in the format
            'YYYY-MM-DD HH:MM:SS').

        Returns
        -------
        None
        """
        updated = (
            DiscordUser(
                username = new_username
            )
            .where(
                DiscordUser.discord_id == discord_id
            )
        .execute()
        )
        return updated > 0
            

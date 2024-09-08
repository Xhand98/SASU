import sqlite3
from NewSimpleSQL.SimpleSQLite import Database, ID
from datetime import datetime
import shutil
import os


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
    def __init__(self, db_path):
        """
        Initializes a DatabaseManager object.
        self.db_path = db_path
        Parameters
        ----------
        db_path : str
            The path to the database file.

        Attributes
        ----------
        self.db_path : str
            The path to the database file.
        self.conn : sqlite3.Connection | None
            The SQLite connection object.
        self.db : NewSimpleSQL.SimpleSQLite.Database | None
            The database object.
        """
        self.db_path = db_path
        self.conn = None
        self.db = None

    def connect(self):
        """
        Establishes a connection to the database.

        Returns
        -------
        None
        """
        self.conn = sqlite3.connect(self.db_path)
        self.db = Database(self.conn)

    def close(self):
        """
        Closes the database connection.

        Returns
        -------
        None
        """
        self.db.close()

    def get_discord(self):
        """
        Retrieves Discord user data.

        Returns
        -------
        list
            A list of tuples containing the Discord ID, username, created_at, and
            updated_at for each user in the database.
        """
        self.db.simple_select_data("discord_users", "*")

    def create_tables(self):
        """
        Creates necessary tables in the database.

        The tables created are:
            - discord_users
            - steam_accounts
            - blacklist

        discord_users contains the following columns:
            - id (auto-incrementing primary key)
            - discord_id (NOT NULL, string)
            - discord_username (NOT NULL, string)
            - created_at (string)
            - updated_at (string)

        steam_accounts contains the following columns:
            - id (auto-incrementing primary key)
            - discord_user_id (NOT NULL, integer, foreign key to discord_users)
            - steam_id (NOT NULL, integer)
            - steam_username (NOT NULL, string)
            - created_at (string)
            - updated_at (string)

        blacklist contains the following columns:
            - id (auto-incrementing primary key)
            - discord_id (NOT NULL, string, foreign key to discord_users)

        The foreign key constraints ensure that a steam account is linked to a
        discord user, and that a discord user is not banned if they are not in the
        discord_users table.
        """
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
        self.db.simple_insert_data(
            "steam_accounts",
            (
                steam_id,
                discord_id,
                steam_username,
                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  # created_at
                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),  # updated_at
            ),
        )
        # Insert data into discord_users table
        self.db.simple_insert_data(
            "discord_users",
            (
                discord_id,
                discord_username,
                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ),
        )

    def get_steam_info(self, discord_id):
        """
        Retrieves Steam account information for a Discord user.

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user to retrieve information for

        Returns
        -------
        list
            A list of dictionaries containing the user's Steam account info
        """
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
        """
        Bans a Discord user from using the bot

        Parameters
        ----------
        discord_id : int
            The Discord ID of the user to ban
        """
        self.db.simple_insert_data(
            "blacklist",
            (discord_id, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))),
        )

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
        if self.db.simple_select_data(
            "blacklist", "discord_id", f"WHERE discord_id = '{discord_id}'"
        ):
            return True
        return False

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
        self.db.simple_delete_data("blacklist", f"discord_id = '{discord_id}'")
        return "User is now unbanned"

    def run_custom_query(self, query):
        """
        Executes a custom SQL query.

        Parameters
        ----------
        query : str
            The SQL query to execute.

        Returns
        -------
        None
        """
        self.db.custom_execute(query)

    def update_user_info(self, discord_id, new_username, date):
        try:
            # Establish a new database connection for this thread
            connection = self.conn
            db = Database(connection)
            # Prepare the update statement with multiple columns
            update_query = """
            UPDATE steam_accounts
            SET steam_id = ?, updated_at = ?
            WHERE discord_user_id = ?
            """
            # Execute the update
            db.custom_execute(update_query, new_username, date, discord_id)
            # Verify the update
            users = db.simple_select_data(
                table="discord_users",
                columns="discord_id, discord_username, updated_at",
                conditions=f"WHERE discord_id = {discord_id}",
                one_fetch=True,
            )
            print("Updated user:", users)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            db.commit()
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

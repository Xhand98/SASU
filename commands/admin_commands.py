import discord
from discord.ext import commands
from db.db_operations import DatabaseOperations as Dbo
from misc.utils import is_authorized


class AdminCommands(commands.Cog):
    """Cog containing commands for administrators to manage the bot.

    This cog contains commands like
    ``/sasuban`` and ``/sasuunban`` to
    ban and unban users from using the bot, respectively.

    All commands in this cog are slash commands and require the
    "Manage Server" permission in order to be used.
    """

    def __init__(self, bot, db_path):
        """
        Initializes an AdminCommands object.

        Parameters
        ----------
        bot : discord.Bot
            The bot instance.
        db_path : str
            The path to the database file.

        Attributes
        ----------
        self.bot : discord.Bot
            The bot instance.
        self.db_operations : DatabaseOperations
            The database operations object.
        """
        self.bot = bot
        self.db_operations = Dbo(db_path)

    @commands.slash_command(name="sasuban", description="Bans user from using the bot.")
    async def sasuban_command(
        self, ctx: discord.ApplicationContext, member: discord.Member
    ):
        """Bans a user from using the bot.

        Parameters
        ----------
        ctx : discord.ApplicationContext
            The interaction context.
        member : discord.Member
            The member to ban.

        Returns
        -------
        None
        """
        if not await is_authorized(ctx.author):
            await ctx.respond("You are not allowed to use this command.")
            return

        try:
            await ctx.defer()
            await self.db_operations.ban_user(member.id)
            await ctx.respond("Banned user!")
        except Exception as e:
            await ctx.respond(f"An error occurred: {e}")

    @commands.slash_command(
        name="sasuunban", description="Unbans user from using the bot."
    )
    async def sasuunban_command(
        self, ctx: discord.ApplicationContext, member: discord.Member
    ):
        """Unbans a user from using the bot.

        Parameters
        ----------
        ctx : discord.ApplicationContext
            The interaction context.
        member : discord.Member
            The member to unban.

        Returns
        -------
        None
        """

        if not await is_authorized(ctx.author):
            await ctx.respond("You are not allowed to use this command.")
            return

        try:
            await ctx.defer()
            await self.db_operations.unban_user(member.id)
            await ctx.respond("Unbanned user!")
        except Exception as e:
            await ctx.respond(f"An error occurred: {e}")

    @commands.slash_command(name="sasubackup", description="Backs up database.")
    async def sasubackup_command(self, ctx: discord.ApplicationContext):
        """Backs up the database.

        This command will backup the database to a
        file named "backup.db" in the
        same directory as the bot. The backup file
        will contain all the data in
        the database, including the SteamIDs of all
        linked users.

        Parameters
        ----------
        ctx : discord.ApplicationContext
            The interaction context.

        Returns
        -------
        None
        """
        if not await is_authorized(ctx.author):
            await ctx.respond("You are not allowed to use this command.")
            return

        try:
            await ctx.defer()
            self.db_operations.backup_database()
            await ctx.respond("The database has been backed up!")
        except Exception as e:
            await ctx.respond(f"An error occurred: {e}")


# Add other admin commands here

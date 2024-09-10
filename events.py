import discord
from discord.ext import commands
from db.db_operations import DatabaseOperations


class EventHandlers(commands.Cog):
    """
    A class containing event handlers for the bot.

    Attributes
    ----------
    self.bot : discord.Bot
        The bot instance.
    self.db_operations : DatabaseOperations
        The database operations object.

    Methods
    -------
    on_ready(self)
        Called when the bot becomes ready.
    verify_banned(self, ctx: discord.ApplicationContext)
        Checks if the user is banned from using the bot before
        each command invocation.
    """

    def __init__(self, bot, db_path):
        """
        Initializes an EventHandlers object.

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
        self.db_operations = DatabaseOperations(db_path)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Called when the bot becomes ready.

        Prints a message to the console
        indicating that the bot is ready and
        online, and then sets the bot to invoke
        the verify_banned function
        before each command invocation.

        This is a discord.py event handler,
        and does not need to be called
        manually. The function is called
        automatically when the bot becomes
        ready.
        """
        print(f"{self.bot.user} is ready and online!")
        self.bot.before_invoke(self.verify_banned)

    async def verify_banned(self, ctx: discord.ApplicationContext):
        """
        Checks if the user is banned from using
        the bot before each command invocation

        If the user is banned, send a message to
        the user and prevent the command from executing.

        This is a discord.py event handler,
        and does not need to be called
        manually. The function is called
        automatically when a command is invoked.
        """

        if await self.db_operations.is_banned(ctx.author.id):
            await ctx.respond("You are banned from using this bot.")
            return


# Add other event handlers here

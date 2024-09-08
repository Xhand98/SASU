import discord
from discord.ext import commands
from db.db_operations import DatabaseOperations

class EventHandlers(commands.Cog):
    def __init__(self, bot, db_path):
        self.bot = bot
        self.db_operations = DatabaseOperations(db_path)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} is ready and online!")
        self.bot.before_invoke(self.verify_banned)

    async def verify_banned(self, ctx: discord.ApplicationContext):
        if await self.db_operations.is_banned(ctx.author.id):
            await ctx.respond("You are banned from using this bot.")
            return

# Add other event handlers here
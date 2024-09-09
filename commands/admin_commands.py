import discord
from discord.ext import commands
from db.db_operations import DatabaseOperations as Dbo
from misc.utils import is_authorized


class AdminCommands(commands.Cog):
    def __init__(self, bot, db_path):
        self.bot = bot
        self.db_operations = Dbo(db_path)

    @commands.slash_command(name="sasuban", description="Bans user from using the bot.")
    async def sasuban_command(
        self, ctx: discord.ApplicationContext, member: discord.Member
    ):
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

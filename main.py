import discord
import os
from dotenv import load_dotenv
from events import EventHandlers
from commands.admin_commands import AdminCommands
from commands.user_commands import UserCommands

load_dotenv()
bot = discord.Bot()

db_path = "./db/users.db"

bot.add_cog(EventHandlers(bot, db_path))
bot.add_cog(AdminCommands(bot, db_path))
bot.add_cog(UserCommands(bot, db_path))

bot.run(os.getenv("TOKEN"))
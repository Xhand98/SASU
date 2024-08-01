import sqlite3
from NewSimpleSQL import Database
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
import datetime
import getrequests.getinfo as getinfo
import misc.embed as embed
import getrequests.getgameico as getgameico
import getrequests.getachievements as getachievements

load_dotenv()  # Load all the variables from the env file
bot = discord.Bot()

async def process_user_or_steamid(user_input):
    if user_input.isdigit() and len(user_input) == 17:
        return user_input  # SteamID
    else:
        try:
            return await getinfo.get_steamid(user_input)
        except Exception as e:
            print(f"Error resolving SteamID: {e}")
            return None


async def get_steamh(res):
    try:
        return await getinfo.get_hours(res)
    except Exception as e:
        print(f"Error getting hours: {e}")
        return None

async def get_steamid_from_db(discord_id):
    connect = sqlite3.connect('steam_users.db')
    db = Database(connect)
    result = db.simple_select_data("users", "steam_id", f"WHERE discord_id = '{discord_id}'", one_fetch=True)
    db.close()
    if result:
        return result[0]
    return None

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="gethours", description="Get hours of a Steam user across all its games.")
async def gethours_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        hours = await get_steamh(steamid)
        if hours:
            await ctx.respond(f"You have {hours:.2f} hours in Steam.")
        else:
            await ctx.respond(f"Couldn't find your hours.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="getsteamid", description="Get the Steam ID of the user.")
async def getsteamid_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        await ctx.respond(f"Your SteamID is {steamid}.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="getgames", description="Get the number of all the games a user owns.")
async def getgames_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        games = await getinfo.get_games(steamid)
        if games:
            await ctx.respond(f"You own {games} games.")
        else:
            await ctx.respond(f"Couldn't find the number of games.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="getpfp", description="Get the profile picture of the user.")
async def getpfp_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        pic_data = await getinfo.get_pic(steamid)
        if pic_data and pic_data.get('avatar'):
            await ctx.respond(f"{pic_data['avatar']}")
        else:
            await ctx.respond(f"Couldn't find your profile picture.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="getlink", description="Get the link to the user's profile.")
async def getlink_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        pic_data = await getinfo.get_pic(steamid)
        if pic_data and pic_data.get('profileurl'):
            await ctx.respond(f"{pic_data['profileurl']}")
        else:
            await ctx.respond(f"Couldn't find your profile link.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="getlevel", description="Get the level of the user.")
async def getlevel_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        level = await getinfo.get_level(steamid)
        if level is not None:
            await ctx.respond(f"You are at level {level}.")
        else:
            await ctx.respond(f"Couldn't find your level.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="getbadges", description="Get the number of badges a user has.")
async def getbadges_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        badges = await getinfo.get_badges(steamid)
        if badges is not None:
            await ctx.respond(f"You have {badges} badges.")
        else:
            await ctx.respond(f"Couldn't find your badges.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="getcountry", description="Get the country of the user.")
async def getcountry_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        country = await getinfo.get_country(steamid)
        if country:
            await ctx.respond(f"You are from {country}.")
        else:
            await ctx.respond(f"Couldn't find your country.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="getuser", description="Get a preview of a user's profile.")
async def getuser_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        try:
            inicio = time.perf_counter()
            steamhresult = await get_steamh(steamid)
            user_games = await getinfo.get_games(steamid)
            pic_data = await getinfo.get_pic(steamid)
            user_name = pic_data.get('personaname')
            user_link = pic_data.get('profileurl')
            level = await getinfo.get_level(steamid)
            badges = await getinfo.get_badges(steamid)
            country = await getinfo.get_country(steamid)
            # achievements = await getachievements.get_player_games(steamid)
            coso = embed.create_embed(
                'User info',
                'Preview of a user’s profile',
                discord.Color.from_rgb(27, 40, 56),
                (user_name, pic_data.get('avatar')),
                (f'Steam link: {user_link}', pic_data.get('avatar')),
                [
                    ('Total hours:', f'{steamhresult:.2f}' if steamhresult else 'N/A', True),
                    ('Total games:', f'{user_games} games' if user_games else 'N/A', True),
                    ('User level:', f'{level}' if level else 'N/A', True),
                    ('\u200B', '\u200B', False),
                    ('Other info', '', False, [
                        ('User badges:', f'{badges}' if badges else 'N/A', True),
                        ('User country:', f'{country}' if country else 'N/A', True),
                        ('Achievements:', f'Soon', True)
                    ]),
                    ('\u200B', '\u200B', True)
                ]
            )
            final = time.perf_counter()
            print(f"se tomo {final - inicio:.2f} segundos")
            await ctx.respond(embed=coso)
        except Exception as e:
            print(f"Error getting user info: {e}")
            await ctx.respond(f"Couldn't retrieve your information.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="getlatestgame", description="Get Latest game of a user.")
async def getlatestgame_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        ico = await getgameico.ejecutar(steamid)
        if ico is not None:
            await ctx.respond(f"{ico}")
        else:
            await ctx.respond(f"Couldn't find your latest game.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="unixtonormal", description="Converts a Unix date and makes it a standard one.")
async def unixconver_command(ctx: discord.ApplicationContext, *, message):
    await ctx.defer()
    message = int(message)
    if message:
        date = datetime.datetime.fromtimestamp(message)
        date_utc = datetime.datetime.fromtimestamp(message, tz=datetime.timezone.utc)
        date_local = datetime.datetime.fromtimestamp(message)
        response = (
            f"**Fecha:**\n"
            f"**UTC Time:** {date_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"**Local Time:** {date_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')}\n"
            f"**ISO 8601:** {date_utc.isoformat()}Z"
        )
        if date is not None:
            await ctx.respond(f"{response}")
        else:
            await ctx.respond(f"Couldn't convert {message} to normal.")
    else:
        await ctx.respond(f"Bruh, {message} ain't no Unix date lmao.")

@bot.slash_command(name="getachievements", description="Gets the number of achievements a player has unlocked.")
async def getachievements_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    steamid = await get_steamid_from_db(str(ctx.author.id))
    if steamid:
        achievements = await getachievements.get_player_games(steamid)
        if achievements is not None:
            await ctx.respond(f"You have unlocked {achievements} achievements.")
        else:
            await ctx.respond(f"Couldn't find your achievements.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="setup", description="Sets up user for the use of the bot.")
async def setup_command(ctx: discord.ApplicationContext, *, message):
    await ctx.defer()
    steamid = await process_user_or_steamid(message)
    discordid = str(ctx.author.id)
    if steamid:
        connect = sqlite3.connect('steam_users.db')
        db = Database(connect)
        db.simple_insert_data("users", (discordid, steamid))
        db.close()
        await ctx.respond(f"Your SteamID {steamid} has been linked to {ctx.author}.")
    else:
        await ctx.respond(f"Invalid SteamID or user {message} not found.")

@bot.slash_command(name="showinfo", description="Shows information for the user.")
async def showinfo_command(ctx: discord.ApplicationContext):
    await ctx.defer()
    discordid = str(ctx.author.id)
    connect = sqlite3.connect('steam_users.db')
    db = Database(connect)
    result = db.simple_select_data("users", "steam_id", f"WHERE discord_id = '{discordid}'", one_fetch=True)
    db.close()
    if result:
        steam_id = result[0]
        await ctx.send(f"The SteamID linked to your Discord is: {steam_id}")
    else:
        await ctx.send("You have not linked your Steam account with the bot.")

bot.run(os.getenv("TOKEN"))

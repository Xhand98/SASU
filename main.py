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

async def get_steamh(res):
    try:
        return await getinfo.get_hours(res)
    except Exception as e:
        print(f"Error getting hours: {e}")
        return None

async def process_user_or_steamid(user_input):
    if user_input.isdigit() and len(user_input) == 17:
        return user_input  # SteamID
    else:
        try:
            return await getinfo.get_steamid(user_input)
        except Exception as e:
            print(f"Error resolving SteamID: {e}")
            return None

async def get_steamid_from_db(discord_id):
    connect = sqlite3.connect('steam_users.db')
    db = Database(connect)
    result = db.simple_select_data("users", "steam_id", f"WHERE discord_id = '{discord_id}'", one_fetch=True)
    db.close()
    return result[0] if result else None

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="gethours", description="Get hours of a Steam user across all its games.")
async def gethours_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        hours = await get_steamh(steamid)
        if hours:
            await ctx.respond(f"{steamid} has {hours:.2f} hours in Steam.")
        else:
            await ctx.respond(f"Couldn't find hours for SteamID {steamid}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

@bot.slash_command(name="getsteamid", description="Get the Steam ID of a user.")
async def getsteamid_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        await ctx.respond(f"SteamID is {steamid}.")
    else:
        await ctx.respond(f"Couldn't find SteamID.")

@bot.slash_command(name="getgames", description="Get the number of all the games a user owns.")
async def getgames_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        games = await getinfo.get_games(steamid)
        if games:
            await ctx.respond(f"{steamid} owns {games} games.")
        else:
            await ctx.respond(f"Couldn't find the number of games for SteamID {steamid}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

@bot.slash_command(name="getpfp", description="Get the profile picture of a user.")
async def getpfp_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        pic_data = await getinfo.get_pic(steamid)
        if pic_data and pic_data.get('avatar'):
            await ctx.respond(f"{pic_data['avatar']}")
        else:
            await ctx.respond(f"Couldn't find profile picture for SteamID {steamid}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

@bot.slash_command(name="getlink", description="Get the link to a user's profile.")
async def getlink_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        pic_data = await getinfo.get_pic(steamid)
        if pic_data and pic_data.get('profileurl'):
            await ctx.respond(f"{pic_data['profileurl']}")
        else:
            await ctx.respond(f"Couldn't find profile link for SteamID {steamid}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

@bot.slash_command(name="getlevel", description="Get the level of a user.")
async def getlevel_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        level = await getinfo.get_level(steamid)
        if level is not None:
            await ctx.respond(f"User at SteamID {steamid} is at level {level}.")
        else:
            await ctx.respond(f"Couldn't find the level for SteamID {steamid}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

@bot.slash_command(name="getbadges", description="Get the number of badges a user has.")
async def getbadges_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        badges = await getinfo.get_badges(steamid)
        if badges is not None:
            await ctx.respond(f"SteamID {steamid} has {badges} badges.")
        else:
            await ctx.respond(f"Couldn't find the badges for SteamID {steamid}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

@bot.slash_command(name="getcountry", description="Get the country of a user.")
async def getcountry_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        country = await getinfo.get_country(steamid)
        if country:
            await ctx.respond(f"SteamID {steamid} is from {country}.")
        else:
            await ctx.respond(f"Couldn't find the country for SteamID {steamid}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

@bot.slash_command(name="getuser", description="Get a preview of a user's profile.")
async def getuser_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
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
            achievements = await getachievements.get_player_games(steamid)
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
                        ('Achievements:', f'{achievements}', True)
                    ]),
                    ('\u200B', '\u200B', True)
                ]
            )
            final = time.perf_counter()
            print(f"se tomo {final - inicio:.2f} segundos")
            await ctx.respond(embed=coso)
        except Exception as e:
            print(f"Error getting user info: {e}")
            await ctx.respond(f"Couldn't retrieve information for SteamID {steamid}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

@bot.slash_command(name="getlatestgame", description="Get Latest game of a user.")
async def getlatestgame_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        ico = await getgameico.ejecutar(steamid)
        if ico is not None:
            await ctx.respond(f"Latest game icon: {ico}")
        else:
            await ctx.respond(f"Couldn't find the latest game for SteamID {steamid}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

@bot.slash_command(name="unixconvert", description="Converts a Unix date and makes it a standard one.")
async def unixconvert_command(ctx: discord.ApplicationContext, *, timestamp: str):
    await ctx.defer()
    try:
        message = int(timestamp)
        date = datetime.datetime.fromtimestamp(message)
        date_utc = datetime.datetime.fromtimestamp(message, tz=datetime.timezone.utc)
        date_local = datetime.datetime.fromtimestamp(message)
        response = (
            f"**Date:**\n"
            f"**UTC Time:** {date_utc.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"**Local Time:** {date_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')}\n"
            f"**ISO 8601:** {date_utc.isoformat()}Z"
        )
        await ctx.respond(f"{response}")
    except ValueError:
        await ctx.respond(f"Invalid Unix timestamp: {timestamp}")

@bot.slash_command(name="getachievements", description="Gets the number of achievements a player has unlocked.")
async def getachievements_command(ctx: discord.ApplicationContext, *, steamid: str = None):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
    steamid = await process_user_or_steamid(steamid)
    if steamid:
        achievements = await getachievements.get_player_games(steamid)
        if achievements is not None:
            await ctx.respond(f"You have unlocked {achievements} achievements.")
        else:
            await ctx.respond(f"Couldn't find your achievements.")
    else:
        await ctx.respond("Your SteamID is not linked.")

@bot.slash_command(name="setup", description="Sets up user for the use of the bot.")
async def setup_command(ctx: discord.ApplicationContext, *, steamid: str):
    await ctx.defer()
    steamid = await process_user_or_steamid(steamid)
    discordid = str(ctx.author.id)
    if steamid:
        connect = sqlite3.connect('steam_users.db')
        db = Database(connect)
        db.simple_insert_data("users", (discordid, steamid))
        db.close()
        await ctx.respond(f"Your SteamID {steamid} has been linked to {ctx.author}.")
    else:
        await ctx.respond(f"Invalid SteamID or user not found.")

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

@bot.slash_command(name="tutorial", description="Guide on how to set up your Steam account with the bot.")
async def tutorial_command(ctx: discord.ApplicationContext, language: str = 'es'):
    await ctx.defer()
    
    # Default to Spanish if no language is specified or the language is invalid
    if language.lower() not in ['es', 'en']:
        language = 'es'
    
    if language == 'en':
        tutorial_text = (
            "**Welcome to the Steam Bot Setup Tutorial!**\n\n"
            "**1. Setting Up Your SteamID**\n"
            "To link your Steam account with the bot, you'll need to provide your SteamID. Here's how you can do it:\n"
            "1. **Find Your SteamID:**\n"
            "   - If you already know your SteamID, you can skip this step. Otherwise, use one of the following methods:\n"
            "     - **Method 1:** Use the SteamID Finder tool available online (search for 'SteamID Finder' on your preferred search engine).\n"
            "     - **Method 2:** Open your Steam profile in a browser and look at the URL. If the URL contains a long number, that is your SteamID. If not, you might need to use the SteamID Finder tool.\n\n"
            "**2. Linking Your SteamID with the Bot**\n"
            "Once you have your SteamID, you can link it to your Discord account using the following command:\n"
            "`/setup steamid:<your_steamid>`\n"
            "Replace `<your_steamid>` with your actual SteamID.\n\n"
            "**3. Verifying Your Setup**\n"
            "To check if your SteamID is successfully linked, use the following command:\n"
            "`/showinfo`\n"
            "The bot will respond with your linked SteamID if everything is set up correctly.\n\n"
            "**4. Using Other Commands**\n"
            "Now that your SteamID is linked, you can use other commands to get information about your Steam profile. For example:\n"
            "`/gethours` - Get total hours played across all your games.\n"
            "`/getgames` - Get the number of games you own.\n"
            "`/getlevel` - Get your Steam level.\n"
            "`/getbadges` - Get the number of badges you have.\n"
            "`/getcountry` - Get your country.\n"
            "`/getuser` - Get a preview of your Steam profile.\n"
            "`/getlatestgame` - Get the icon of your latest game.\n"
            "`/getachievements` - Get the number of achievements you have unlocked.\n\n"
            "**Need More Help?**\n"
            "If you need further assistance, feel free to ask in the support channel or reach out to the bot developers."
        )
    else:  # Spanish by default or if language is 'es'
        tutorial_text = (
            "# ¡Bienvenido al Tutorial de Configuración del Bot de Steam!**\n\n"
            "##1. Configuración de tu SteamID**\n"
            "Para vincular tu cuenta de Steam con el bot, necesitarás proporcionar tu SteamID. Aquí tienes cómo hacerlo:\n"
            "1. ##Encuentra tu SteamID:**\n"
            "   - Si ya conoces tu SteamID, puedes omitir este paso. De lo contrario, usa uno de los siguientes métodos:\n"
            "     - ###Método 1: Usa la herramienta de SteamID Finder disponible en línea (busca 'SteamID Finder' en tu motor de búsqueda preferido).\n"
            "     - **Método 2:** Abre tu perfil de Steam en un navegador y mira la URL. Si la URL contiene un número largo, ese es tu SteamID. Si no, es posible que necesites usar la herramienta SteamID Finder.\n\n"
            "**2. Vinculando tu SteamID con el Bot**\n"
            "Una vez que tengas tu SteamID, puedes vincularlo a tu cuenta de Discord usando el siguiente comando:\n"
            "`/setup steamid:<tu_steamid>`\n"
            "Reemplaza `<tu_steamid>` con tu SteamID real.\n\n"
            "**3. Verificando tu Configuración**\n"
            "Para verificar si tu SteamID está vinculado correctamente, usa el siguiente comando:\n"
            "`/showinfo`\n"
            "El bot responderá con tu SteamID vinculado si todo está configurado correctamente.\n\n"
            "**4. Usando Otros Comandos**\n"
            "Ahora que tu SteamID está vinculado, puedes usar otros comandos para obtener información sobre tu perfil de Steam. Por ejemplo:\n"
            "`/gethours` - Obtén el total de horas jugadas en todos tus juegos.\n"
            "`/getgames` - Obtén el número de juegos que posees.\n"
            "`/getlevel` - Obtén tu nivel de Steam.\n"
            "`/getbadges` - Obtén el número de medallas que tienes.\n"
            "`/getcountry` - Obtén tu país.\n"
            "`/getuser` - Obtén una vista previa de tu perfil de Steam.\n"
            "`/getlatestgame` - Obtén el ícono de tu juego más reciente.\n"
            "`/getachievements` - Obtén el número de logros que has desbloqueado.\n\n"
            "**¿Necesitas Más Ayuda?**\n"
            "Si necesitas más asistencia, no dudes en preguntar en el canal de soporte o contactar a los desarrolladores del bot."
        )
    
    await ctx.respond(tutorial_text)


bot.run(os.getenv("TOKEN"))

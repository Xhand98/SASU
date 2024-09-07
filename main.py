import re
import discord
import os
from dotenv import load_dotenv
import time

from db.dbmanager import DatabaseManager as Dbm
import getrequests.getachievements as getachievements
import getrequests.getgameico as getgameico
import getrequests.getinfo as getinfo
import misc.embed as embed

import asyncio

load_dotenv()
bot = discord.Bot()
AUTHORIZED_USER_IDS = [543132514848604170, 987654321012345678]


def normalize_data(data):
    """Ensures all tuples have the same number of elements by adding placeholders if necessary."""
    max_length = max(len(item) for item in data)
    normalized_data = [
        (
            item + ("placeholder",) * (max_length - len(item))
            if len(item) < max_length
            else item
        )
        for item in data
    ]
    return normalized_data


async def check_user(steamid, ctx: discord.ApplicationContext):
    """Checks if a user has a SteamID associated with their Discord ID in the database.

    If the user has a SteamID associated, it returns the SteamID, otherwise it returns None.

    Parameters:
    steamid (int | str): The SteamID to check.
    ctx (discord.ApplicationCommand): The Discord command context.

    Returns:
    int | str | None: The SteamID if the user has one, otherwise None.
    """
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
        steamid = steamid[0][0]
    steamid = await process_user_or_steamid(steamid)
    return steamid


async def get_steamid_from_db(discord_id: str):
    """Gets the SteamID associated with a Discord ID from the database

    Parameters
    ----------
    discord_id : int
        The Discord ID of the user to get the SteamID for

    Returns
    -------
    list
        A list of tuples containing the SteamID, Discord ID, and Discord username
        of the user. If the user is not found in the database, an empty list is
        returned.
    """
    db = Dbm(db_path="./db/users.db")
    db.connect()
    data = db.get_steam_info(discord_id)
    db.close()
    return data


async def is_banned(discord_id):
    """Checks if a user is banned from using the bot

    Args:
        discord_id (int): The Discord ID of the user

    Returns:
        bool: True if the user is banned, False otherwise
    """
    if discord_id:
        db = Dbm(db_path="./db/users.db")
        db.connect()
        queso = db.isbanned(discord_id)
        db.close()
        return queso


async def is_authorized(user: discord.User) -> bool:
    """Checks if the user has authorization to use the command"""
    return user.id in AUTHORIZED_USER_IDS


async def user_info(steamid):
    """Get the username of a Steam user from their SteamID.

    Args:
        steamid: The SteamID of the user.

    Returns:
        The username of the user if the SteamID is valid,
        otherwise "User not found or data is private".
    """
    pic_data = await getinfo.get_pic(steamid)
    if pic_data:  # Check if pic_data is not None
        user_name = pic_data.get("personaname")
        return user_name

    return "User not found or data is private"


async def get_steamh(res):
    """Get the total hours of a Steam user across all games.

    Args:
        res: SteamID to get the hours from.

    Returns:
        The total hours if successful, None otherwise.
    """
    try:
        return await getinfo.get_hours(res)
    except Exception as e:
        print(f"Error getting hours: {e}")
        return None


async def process_user_or_steamid(user_input: str):
    """Process a user input to get a SteamID.

    Args:
        user_input (str): Input to process. Can be a SteamID, a username, or a URL to a Steam profile.

    Returns:
        str: SteamID, or None if an error occurred.
    """
    user_input = str(user_input)
    if user_input.isdigit() and len(user_input) == 17:
        return user_input  # SteamID

    return await getinfo.get_steamid(user_input)


async def verify_banned(ctx: discord.ApplicationContext):
    """Check if the user is banned from using the bot before each command invocation

    If the user is banned, send a message to the user and prevent the command from executing.
    """
    if await is_banned(ctx.author.id):
        await ctx.respond("You are banned from using this bot.")
        return


# region ON READY
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    bot.before_invoke(verify_banned)


@bot.slash_command(
    name="gethours", description="Get hours of a Steam user across all its games."
)
async def gethours_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    """
    Get hours of a Steam user across all its games.

    Args:
        ctx (discord.ApplicationContext): The context of the slash command.
        steamid (str | None): The SteamID of the user to get hours for. If None, the user linked to the Discord account will be used.
    """
    await ctx.defer()
    try:
        if steamid is None:
            steamid = await get_steamid_from_db(str(ctx.author.id))
            steamid = str(steamid[0][0])
            steamid = await check_user(steamid, ctx)
        else:
            # print(steamid)
            steamid = str(steamid)
            steamid = await check_user(steamid, ctx)
            # print(steamid)

        if steamid:
            hours = await get_steamh(steamid)
            if hours:
                user_name = await user_info(steamid)
                result = discord.Embed(
                    title=f"{user_name}'s Hours",
                    description=f"{user_name} has {round(hours, 2)} hours.",
                    color=discord.Color.random(),
                )
                result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond(f"Couldn't find hours for SteamID {steamid}.")
        else:
            await ctx.respond("Invalid SteamID or user not found.")
    except Exception as e:
        await ctx.respond(f"An error occurred while processing your request {e}.")


@bot.slash_command(name="getsteamid", description="Get the Steam ID of a user.")
async def getsteamid_command(
        ctx: discord.ApplicationContext, *, steamurl: str | None = None
):
    """
    Gets the Steam ID of a user, either from the database if no URL is provided
    or from the given URL if it is a valid Steam profile URL.

    Args:
        ctx (discord.ApplicationContext): The context of the invoked command.
        steamurl (str | None): The URL of the Steam profile to get the Steam ID of.
            If None, the Steam ID will be retrieved from the database for the
            user who invoked the command.

    Returns:
        None
    """
    await ctx.defer()

    if steamurl is None:
        data = await get_steamid_from_db(str(ctx.author.id))
        steamid = data[0][2]
        if steamid:
            user_name = await user_info(steamid)

            result = discord.Embed(
                title=f"{user_name}'s Steam ID",
                description=f"{user_name}'s Steam ID is {steamid}",
                color=discord.Color.random(),
            )
            result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            await ctx.respond(embed=result)
        else:
            await ctx.respond("No Steam ID found in the database for your account.")
        return

    match = re.search(
        r"(?:https?://)?steamcommunity\.com/(?:id|profiles)/([^/]+)", steamurl
    )

    if match:
        steamid_or_username = match.group(1)
    else:
        steamid_or_username = steamurl

    steamid = await process_user_or_steamid(steamid_or_username)

    user_name = await user_info(steamid)

    result = discord.Embed(
        title=f"{user_name}'s Steam ID",
        description=f"{user_name}'s Steam ID is {steamid}",
        color=discord.Color.random(),
    )
    result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
    await ctx.respond(embed=result)


@bot.slash_command(
    name="getgames", description="Get the number of all the games a user owns."
)
async def getgames_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    """
    Get the number of all the games a user owns.

    Args:
        ctx: The interaction object.
        steamid: The SteamID of the user to get the number of games for. If not provided, the SteamID of the user running the command is used.

    Returns:
        None
    """
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
        steamid = await check_user(steamid, ctx)
    else:
        steamid = await check_user(steamid, ctx)

    if steamid:
        games = await getinfo.get_games(steamid)
        if games:
            user_name = await user_info(steamid)
            result = discord.Embed(
                title=f"{user_name}'s Games",
                description=f"{user_name} has {games} games.",
                color=discord.Color.random(),
            )
            result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            await ctx.respond(embed=result)
        else:
            await ctx.respond(
                f"Couldn't find the number of games for SteamID {steamid}."
            )
    else:
        await ctx.respond("Invalid SteamID or user not found.")


@bot.slash_command(name="getpfp", description="Get the profile picture of a user.")
async def getpfp_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
        steamid = await check_user(steamid, ctx)
    else:
        steamid = await check_user(steamid, ctx)

    if steamid:
        pic_data = await getinfo.get_pic(steamid)
        if pic_data and pic_data.get("avatar"):
            avatar = pic_data["avatar"]
            user_name = await user_info(steamid)
            result = discord.Embed(
                title=f"{user_name} Pfp", color=discord.Color.random()
            )
            result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            result.set_image(url=avatar)
            await ctx.respond(result=result)
        else:
            await ctx.respond(f"Couldn't find profile picture for SteamID {steamid}.")
    else:
        await ctx.respond("Invalid SteamID or user not found.")


@bot.slash_command(name="getlink", description="Get the link to a user's profile.")
async def getlink_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    """
    Gets the link to a user's Steam profile.

    Args:
        steamid (str, optional): The SteamID of the user to get the link for. Defaults to None.
        ctx (discord.ApplicationContext): The interaction context.

    Returns:
        discord.Embed: An embed containing the user's Steam profile link.
    """
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
        steamid = await check_user(steamid, ctx)
    else:
        steamid = await check_user(steamid, ctx)

    if steamid:
        pic_data = await getinfo.get_pic(steamid)
        if pic_data and pic_data.get("profileurl"):
            url = pic_data["profileurl"]
            user_name = await user_info(steamid)
            result = discord.Embed(
                title=f"{user_name}'s Link",
                description=f"{user_name}'s link is {url}",
                color=discord.Color.random(),
            )
            result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            await ctx.respond(embed=result)
        else:
            await ctx.respond(f"Couldn't find profile link for SteamID {steamid}.")
    else:
        await ctx.respond("Invalid SteamID or user not found.")


@bot.slash_command(name="getlevel", description="Get the level of a user.")
async def getlevel_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    """
    Gets the level of a user.

    Args:
        ctx (discord.ApplicationContext): The interaction context.
        steamid (str | None, optional): The SteamID of the user to get the level of. Defaults to None.

    Returns:
        discord.InteractionMessage: The interaction message containing the level of the user.
    """
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
        steamid = await check_user(steamid, ctx)
    else:
        steamid = await check_user(steamid, ctx)

    if steamid:
        level = await getinfo.get_level(steamid)
        if level is not None:
            user_name = await user_info(steamid)
            result = discord.Embed(
                title=f"{user_name}'s Level",
                description=f"{user_name}'s level is {level}",
                color=discord.Color.random(),
            )
            result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            await ctx.respond(embed=result)
        else:
            await ctx.respond(f"Couldn't find the level for SteamID {steamid}.")
    else:
        await ctx.respond("Invalid SteamID or user not found.")


@bot.slash_command(name="getbadges", description="Get the number of badges a user has.")
async def getbadges_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    """
    Gets the number of badges a user has.

    Args:
        ctx (discord.ApplicationContext): The context of the command invocation.
        steamid (str | None, optional): The SteamID of the user. If not provided, the SteamID of the user who invoked the command is used.

    Returns:
        discord.InteractionResponse: The response to the command invocation, containing the number of badges the user has.
    """
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
        steamid = await check_user(steamid, ctx)
    else:
        steamid = await check_user(steamid, ctx)

    if steamid:
        badges = await getinfo.get_badges(steamid)
        if badges is not None:
            user_name = await user_info(steamid)
            result = discord.Embed(
                title=f"{user_name}'s Badges",
                description=f"{user_name} has {badges} badges.",
                color=discord.Color.random(),
            )
            result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            await ctx.respond(embed=result)
        else:
            await ctx.respond(f"Couldn't find the badges for SteamID {steamid}.")
    else:
        await ctx.respond("Invalid SteamID or user not found.")


@bot.slash_command(name="getcountry", description="Get the country of a user.")
async def getcountry_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    """
    Gets the country of a user.

    Args:
        ctx (discord.ApplicationContext): The interaction context.
        steamid (str | None, optional): The SteamID of the user to get the country of. Defaults to None.

    Returns:
        discord.InteractionMessage: The interaction message containing the country of the user.
    """
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
        steamid = await check_user(steamid, ctx)
    else:
        steamid = await check_user(steamid, ctx)

    if steamid:
        country = await getinfo.get_country(steamid)
        if country:
            user_name = await user_info(steamid)
            result = discord.Embed(
                title=f"{user_name}'s Country",
                description=f"{user_name}'s lives in {country}",
                color=discord.Color.random(),
            )
            result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            await ctx.respond(embed=result)
        else:
            await ctx.respond(f"Couldn't find the country for SteamID {steamid}.")
    else:
        await ctx.respond("Invalid SteamID or user not found.")


@bot.slash_command(name="getuser", description="Get a preview of a user's profile.")
async def getuser_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    await ctx.defer()
    try:
        if steamid is None:
            steamid_data = await get_steamid_from_db(str(ctx.author.id))
            if not steamid_data:
                await ctx.respond("No SteamID found linked to your Discord account.")
                return
            steamid = str(steamid_data[0][0])

        steamid = await check_user(steamid, ctx)
        if not steamid:
            await ctx.respond("Invalid SteamID or user not found.")
            return

        start_time = time.perf_counter()

        # Fetch user data
        total_hours = await get_steamh(steamid)
        total_games = await getinfo.get_games(steamid)
        user_profile = await getinfo.get_pic(steamid)
        user_name = user_profile.get("personaname", "Unknown User")
        user_avatar = await getinfo.get_pic(steamid)
        user_link = await getinfo.get_pic(steamid)
        user_level = await getinfo.get_level(steamid)
        user_badges = await getinfo.get_badges(steamid)
        user_country = await getinfo.get_country(steamid)
        user_achievements = await getachievements.main(steamid)

        # Create embed
        result = discord.Embed(
            title=f"{user_name}'s Steam Profile",
            description="Here's a quick overview of the user's Steam profile.",
            color=discord.Color.random(),
            url=user_link["profileurl"],
        )

        result.set_thumbnail(url=user_avatar["avatar"])

        # Add fields
        result.add_field(
            name="Total Hours Played",
            value=f"{total_hours:.2f} hours" if total_hours else "Private/Unavailable",
            inline=True,
        )
        result.add_field(
            name="Total Games Owned",
            value=f"{total_games} games" if total_games else "Private/Unavailable",
            inline=True,
        )
        result.add_field(
            name="Steam Level",
            value=f"{user_level}" if user_level else "Private/Unavailable",
            inline=True,
        )
        result.add_field(
            name="Badges",
            value=f"{user_badges}" if user_badges else "Private/Unavailable",
            inline=True,
        )
        result.add_field(
            name="Country",
            value=f"{user_country}" if user_country else "Private/Unavailable",
            inline=True,
        )
        result.add_field(
            name="Total Achievements",
            value=(
                f"{user_achievements}" if user_achievements else "Private/Unavailable"
            ),
            inline=True,
        )

        # Send embed
        await ctx.respond(embed=result)

        end_time = time.perf_counter()
        print(f"Execution took {end_time - start_time:.2f} seconds")

    except Exception as e:
        print(f"Error getting user info: {e}")
        await ctx.respond("An error occurred while retrieving the user's information.")


@bot.slash_command(name="getlatestgame", description="Get Latest game of a user.")
async def getlatestgame_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    """
    Get the latest game of a user.

    Args:
        ctx (discord.ApplicationContext): The interaction context.
        steamid (str | None, optional): The SteamID of the user. Defaults to None.

    Returns:
        discord.InteractionMessage: The response message.
    """
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
        steamid = await check_user(steamid, ctx)
    else:
        steamid = await check_user(steamid, ctx)

    if steamid:
        ico = await getgameico.ejecutar(steamid)
        if ico is not None:
            user_name = await user_info(steamid)
            result = discord.Embed(
                title=f"{user_name}'s Latest Game", color=discord.Color.random()
            )
            result.set_image(url=ico)
            result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            await ctx.respond(embed=result)
        else:
            await ctx.respond(f"Couldn't find the latest game for SteamID {steamid}.")
    else:
        await ctx.respond("Invalid SteamID or user not found.")


@bot.slash_command(
    name="getachievements",
    description="Gets the number of achievements a player has unlocked.",
)
async def getachievements_command(
        ctx: discord.ApplicationContext, *, steamid: str | None = None
):
    """Gets the number of achievements a player has unlocked.

    Args:
        steamid (str | None): The SteamID of the user to get the achievements for.
            If None, the SteamID linked to the user who invoked the command is used.
        ctx (discord.ApplicationContext): The context of the slash command.

    Returns:
        A message with the number of achievements the user has unlocked.
        If the user does not have a SteamID linked, a message saying so is sent.
    """
    await ctx.defer()
    if steamid is None:
        steamid = await get_steamid_from_db(str(ctx.author.id))
        steamid = await check_user(steamid, ctx)
    else:
        steamid = await check_user(steamid, ctx)

    if steamid:
        achievements = await getachievements.main(steamid)
        if achievements is not None:
            user_name = await user_info(steamid)
            result = discord.Embed(
                title=f"{user_name}'s Achievements",
                description=f"{user_name} has {achievements} achievements.",
                color=discord.Color.random(),
            )
            result.set_author(name=bot.user.name, icon_url=bot.user.avatar)
            await ctx.respond(embed=result)
        else:
            await ctx.respond("Couldn't find your achievements.")
    else:
        await ctx.respond("Your SteamID is not linked.")


@bot.slash_command(name="setup", description="Sets up user for the use of the bot.")
async def setup_command(ctx: discord.ApplicationContext, *, steamid: str | None = None):
    await ctx.defer()
    if steamid:
        steamid = await process_user_or_steamid(steamid)
        discordid = str(ctx.author.id)
        discordname = ctx.author.name
        pic_data = await getinfo.get_pic(steamid)
        steam_username = pic_data.get("personaname")
        db = Dbm(db_path="./db/users.db")
        db.connect()
        discordid = int(discordid)
        steamid = int(steamid)
        db.link_steam_id(discordid, steamid, steam_username, discordname)

        await ctx.respond(f"Your SteamID {steamid} has been linked to {ctx.author}.")
    else:
        await ctx.respond(
            "If you want to setup the bot to work without putting " +
            "the input, write </tutorial:1275183733116370950>."
        )


@bot.slash_command(name="showinfo", description="Shows information for the user.")
async def showinfo_command(ctx: discord.ApplicationContext):
    """Shows information for the user, such as their SteamID and whether their Steam account is linked with the bot."""
    await ctx.defer()

    try:
        discordid = str(ctx.author.id)

        # Sample data
        info = await get_steamid_from_db(discordid)

        # Normalize data to ensure consistent structure
        info = normalize_data(info)

        # Debug: Print the normalized data structure
        print(f"Normalized data: {info}")

        embedd = discord.Embed(
            title=f"{ctx.author.name}'s Stored Information",
            color=discord.Color.random(),
        )

        if discordid:
            embed.create_embed_tables(embedd, info, default_inline=True)
            if embedd.fields:  # Check if embed has any fields
                await ctx.respond(embed=embedd)
            else:
                await ctx.respond(content="No information available to display.")
        else:
            await ctx.respond(
                content="You have not linked your Steam account with the bot."
            )

    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.respond("An error occurred while processing your request.")


@bot.slash_command(name="simpletest", description="Simple test command.")
async def simpletest_command(ctx: discord.ApplicationContext):
    """Simple test command that simulates some processing delay and responds with a message."""
    await ctx.defer()
    await asyncio.sleep(1)  # Simulate some processing delay
    await ctx.respond("This is a test message.")


@bot.slash_command(
    name="tutorial",
    description="Guide on how to set up your Steam account with the bot.",
)
async def tutorial_command(ctx: discord.ApplicationContext, language: str = "en"):
    """
    Guide on how to set up your Steam account with the bot.

    This command will display a tutorial on how to set up your Steam account with the bot. The tutorial will be in English by default, but you can change the language to Spanish by using the `language` parameter.

    Parameters
    ----------
    language : str
        The language of the tutorial. Can be either "en" for English or "es" for Spanish. Defaults to "en" if not specified.

    Returns
    -------
    None
    :param language:
    :param ctx:
    """
    await ctx.defer()

    if language.lower() not in ["es", "en"]:
        language = "en"

    if language == "en":
        tutorial_text = (
            "# Welcome to the Steam Bot Setup Tutorial!\n\n"
            "## 1. Setting Up Your SteamID\n"
            "To link your Steam account with the bot, you'll need to  "
            "provide your SteamID. Here's how you can do it:\n"
            "### 1. Find Your SteamID:\n"
            "###   - If you already know your SteamID, you can skip this step. "
            "Otherwise, use one of the following methods:\n"
            "      The Method: Open your Steam profile in a browser "
            "and copy the URL and paste it in, </tutorial:1275183733116370950>, "
            "the output is your steamID.\n\n"
            "## 2. Linking Your SteamID with the Bot\n"
            "Once you have your SteamID, you can link it to "
            "your Discord account using the following command:\n"
            "</setup:1275183733116370947> `steamid:<your_steamid>`\n"
            "Replace <your_steamid> with your actual SteamID.\n\n"
            "## 3. Verifying Your Setup\n"
            "To check if your SteamID is successfully linked, "
            "use the following command:\n"
            "</showinfo:1275183733116370949>\n"
            "The bot will respond with your linked SteamID "
            "if everything is set up correctly.\n\n"
            "## 4. Using Other Commands\n"
            "Now that your SteamID is linked, you can use other "
            "commands to get information about "
            "your Steam profile. For example:\n"
            "</gethours:1275183732927758366> - Get total hours played"
            " across all your games.\n"
            "</getgames:1275183732927758368> - Get the number of games you own.\n"
            "</getlevel:1275183732927758371> - Get your Steam level.\n"
            "</getbadges:1275183732927758372> - Get the number of badges you have.\n"
            "</getcountry:1275183732927758374> - Get your country.\n"
            "</getuser:1275183732927758375> - Get a preview of your Steam profile.\n"
            "</getlatestgame:1275183733116370944> - Get the icon of your latest game.\n"
            "</getachievements:1275183733116370946> - Get the number of"
            " achievements you have unlocked.\n\n"
            "# Need More Help?\n"
            "If you need further assistance, feel free to ask in the support channel or"
            " reach out to  <@543132514848604170>."
        )
    else:  # Spanish by default or if language is 'es'
        tutorial_text = (
            "# ¡Bienvenido al Tutorial de Configuración del Bot de Steam!\n\n"
            "## 1. Configuración de tu SteamID\n"
            "Para vincular tu cuenta de Steam con el bot, "
            " necesitarás proporcionar tu SteamID. "
            "Aquí te explicamos cómo hacerlo:\n"
            "### 1. Encuentra tu SteamID:\n"
            "###    - Si ya conoces tu SteamID, puedes "
            "saltarte este paso. De lo contrario, "
            "usa uno de los siguientes métodos:\n"
            "    Método: Abre tu perfil de Steam en un navegador, "
            "copia la URL y pégala en "
            "`/getsteamid`. El resultado será tu SteamID.\n\n"
            "## 2. Vincula tu SteamID con el Bot\n"
            "Una vez que tengas tu SteamID, puedes vincularla "
            "a tu cuenta de Discord usando el siguiente comando:\n"
            "`</setup:1275183733116370947> steamid:<tu_steamid>`\n"
            "Reemplaza `<tu_steamid>` con tu SteamID real.\n\n"
            "## 3. Verifica tu Configuración\n"
            "Para comprobar si tu SteamID se ha "
            "vinculado correctamente, usa el siguiente "
            "comando:\n"
            "`</showinfo:1275183733116370949>`\n"
            "El bot responderá con tu SteamID vinculada "
            "si todo está configurado correctamente.\n\n"
            "## 4. Usar Otros Comandos\n"
            "Ahora que tu SteamID está vinculada, "
            "puedes usar otros comandos para obtener "
            "información sobre tu perfil de Steam. Por ejemplo:\n"
            "`</gethours:1275183732927758366>` - Obtén el total de horas "
            "jugadas en todos tus juegos.\n"
            "`</getgames:1275183732927758368>` - Obtén el número "
            "de juegos que posees.\n"
            "`</getlevel:1275183732927758371>` - Obtén tu nivel de Steam.\n"
            "`</getbadges:1275183732927758372>` - Obtén el número de "
            "insignias que tienes.\n"
            "`</getcountry:1275183732927758374>` - Obtén tu país.\n"
            "`</getuser:1275183732927758375>` - Obtén una vista previa "
            "de tu perfil de Steam.\n"
            "`</getlatestgame:1275183733116370944>` - Obtén el icono de "
            "tu juego más reciente.\n"
            "`</getachievements:1275183733116370946>` - Obtén el número de logros "
            "que has desbloqueado.\n\n"
            "# ¿Necesitas más ayuda?\n"
            "Si necesitas más asistencia, no dudes en preguntar en el canal de soporte o "
            "contactar a cualquier <@543132514848604170> ."
        )

    await ctx.respond(tutorial_text)


@bot.slash_command(name="sasuban", description="Bans user from using the bot.")
async def sasuban_command(ctx: discord.ApplicationContext, member: discord.Member):
    """Ban a user from using the bot.

    Args:
        ctx: The slash command context.
        discordid: The Discord ID of the user to ban.
        :param ctx:
        :param member: The member to ban from using the bot.
        ctx: (discord.ApplicationContext) The slash command context.

    Returns:
        A message indicating whether the user was banned or not.
    """
    if not await is_authorized(ctx.author):
        await ctx.respond("You are not allowed to use this command.")
        return

    try:
        await ctx.defer()
        db = Dbm(db_path="db/users.db")
        db.connect()
        db.ban(member.id)
        db.close()
        await ctx.respond("Banned user!")
    except Exception as e:
        await ctx.respond(f"An error ocurred: {e}")


@bot.slash_command(name="isbanned", description="Check if user is banned.")
async def isbanned_command(ctx: discord.ApplicationContext, member: discord.Member):
    """
    Checks if a user is banned from using the bot.

    Args:
        ctx (discord.ApplicationContext): The slash command context.
        member (discord.Member): The Discord ID of the user to check.

    Returns:
        str: A message indicating whether the user is banned or not.
    """
    await ctx.defer()
    banned = await is_banned(member.id)
    await ctx.respond(banned)


@bot.slash_command(name="sasuunban", description="Unbans user from using the bot.")
async def sasuunban_command(ctx: discord.ApplicationContext, member: discord.Member):
    """
        Unban a user from using the bot.

        Args:
            ctx: The slash command context.
            member: The member to unban from using the bot.

        Returns:
            A message indicating whether the user was unbanned or not.
    """
    if not is_authorized(ctx.author):
        await ctx.respond("You are not allowed to use this command.")
        return

    try:
        await ctx.defer()
        db = Dbm(db_path="db/users.db")
        db.connect()
        db.unban(member.id)
        db.close()
        await ctx.respond("Unbanned user!")
    except Exception as e:
        await ctx.respond(f"An error ocurred: {e}")


@bot.slash_command(name="sasubackup", description="Backs up database.")
async def sasubackup_command(ctx: discord.ApplicationContext):
    """
        Unban a user from using the bot.

        Args:
            ctx: The slash command context.

        Returns:
            A message indicating wheter the daatabase was backeup or not.
    """
    if not await is_authorized(ctx.author):
        await ctx.respond("You are not allowed to use this command.")
        return

    try:
        await ctx.defer()
        db = Dbm(db_path="db/users.db")
        db.connect()
        db.backup_database()
        db.close()
        await ctx.respond("The database has been backed up!")
    except Exception as e:
        await ctx.respond(f"An error ocurred: {e}")


bot.run(os.getenv("TOKEN"))

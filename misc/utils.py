# utils.py
import discord
from getrequests.getinfo import get_steamid, get_pic, get_hours
from db.db_operations import DatabaseOperations as Dbo

AUTHORIZED_USER_IDS = [543132514848604170, 987654321012345678]


def normalize_data(data):
    """
    Ensures all tuples have the same number
    of elements by adding placeholders if necessary.
    """
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


async def process_user_or_steamid(user_input: str):
    """Process a user input to get a SteamID.

    Args:
        user_input (str): Input to process.
        Can be a SteamID, a username,
        or a URL to a Steam profile.

    Returns:
        str: SteamID, or None if an error occurred.
    """
    user_input = str(user_input)
    if user_input.isdigit() and len(user_input) == 17:
        return user_input  # SteamID

    return await get_steamid(user_input)


async def is_authorized(user: discord.User) -> bool:
    """Checks if the user has authorization to use the command"""
    return user.id in AUTHORIZED_USER_IDS


async def check_user(steamid, ctx: discord.ApplicationContext):
    """Checks if a user has a SteamID associated with their Discord ID in the database.

    If the user has a SteamID associated,
    it returns the SteamID, otherwise it returns None.

    Parameters:
    steamid (int | str): The SteamID to check.
    ctx (discord.ApplicationCommand): The Discord command context.

    Returns:
    int | str | None: The SteamID if the user has one, otherwise None.
    """
    db = Dbo('../db/users.db')
    if steamid is None:
        steamid = await db.get_steamid_from_db(str(ctx.author.id))
        steamid = steamid[0][0]
    steamid = await process_user_or_steamid(steamid)
    return steamid


async def user_info(steamid):
    """Get the username of a Steam user from their SteamID.

    Args:
        steamid: The SteamID of the user.

    Returns:
        The username of the user if the SteamID is valid,
        otherwise "User not found or data is private".
    """
    pic_data = await get_pic(steamid)
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
        return await get_hours(res)
    except Exception as e:
        print(f"Error getting hours: {e}")
        return None


async def verify_banned(ctx: discord.ApplicationContext):
    """Check if the user is banned from using the bot before each command invocation

    If the user is banned, send a message to
    the user and prevent the command from executing.
    """
    db = Dbo('../db/users.db')
    if await db.is_banned(ctx.author.id):
        await ctx.respond("You are banned from using this bot.")
        return

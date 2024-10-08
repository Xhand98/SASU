import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()


async def get_levels(user):
    """
    Gets the level of a Steam user.

    Args:
        user: The SteamID of the user to get the level of.

    Returns:
        The level of the user if the request is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = (
        f"https://api.steampowered.com/IPlayerService/GetBadges/v1/"
        f"?key={api_key}"
        f"&steamid={steamuser}"
        f"&skip_unvetted_apps=0"
        f"&include_appinfo=1"
        f"&include_played_free_games=1"
        f"&include_free_sub=1"
    )

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            info = data["response"]["player_level"]
        else:
            print(f"Error al obtener los datos: {response.status}")
            info = None
    return info


async def get_badges(user):
    """
    Gets the number of badges a Steam user has.

    Args:
        user: The SteamID of the user to get the number of badges of.

    Returns:
        The number of badges the user has if the request is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = (
        f"https://api.steampowered.com/IPlayerService/GetBadges/v1/"
        f"?key={api_key}"
        f"&steamid={steamuser}"
        f"&skip_unvetted_apps=0"
        f"&include_appinfo=1"
        f"&include_played_free_games=1"
        f"&include_free_sub=1"
    )

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            info = len(data["response"]["badges"])
        else:
            print(f"Error al obtener los datos: {response.status}")
            info = None
    return info

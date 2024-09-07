import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()


async def get_levels(user):
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = f"https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={api_key}&steamid={steamuser}&skip_unvetted_apps=0&include_appinfo=1&include_played_free_games=1&include_free_sub=1"

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            info = data["response"]["player_level"]
        else:
            print(f"Error al obtener los datos: {response.status}")
            info = None
    return info


async def get_badges(user):
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = f"https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={api_key}&steamid={steamuser}&skip_unvetted_apps=0&include_appinfo=1&include_played_free_games=1&include_free_sub=1"

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            info = len(data["response"]["badges"])
        else:
            print(f"Error al obtener los datos: {response.status}")
            info = None
    return info

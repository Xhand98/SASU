import aiohttp
import os


async def ejecutar(user):
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = f"https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={api_key}&steamid={user}&skip_unvetted_apps=0"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                info = data["response"]["player_level"]
            else:
                print(f"Error al obtener los datos: {response.status}")
                info = None
    return info

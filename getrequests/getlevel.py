import aiohttp
import os


async def ejecutar(user):
    """
    Gets the level of a Steam user.

    Args:
        user: The SteamID of the user to get the level of.

    Returns:
        The level of the user if the request is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")

    url: str = (f"https://api.steampowered.com/IPlayerService/GetBadges/v1/"
                f"?key={api_key}&steamid={user}&skip_unvetted_apps=0")

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            info = data["response"]["player_level"]
        else:
            print(f"Error al obtener los datos: {response.status}")
            info = None
    return info

import aiohttp
import os


async def ejecutar(user):
    """
    Gets the total hours of a Steam user across all of their games.

    Args:
        user: The SteamID of the user to get the total hours for.

    Returns:
        The total hours played by the user if the request
        is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")
    steam_id = user

    url = (f"http://api.steampowered.com/IPlayerService/GetOwnedGames"
           f"/v0001/?key={api_key}&steamid={steam_id}&format=json")

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            total_playtime_minutes = sum(
                game["playtime_forever"] for game in data["response"]["games"]
            )
            total_playtime_hours = total_playtime_minutes / 60
            user = f"{total_playtime_hours:.2f} hours"
        else:
            print(f"Error al obtener los datos: {response.status}")
            user = None
    return user

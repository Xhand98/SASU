import aiohttp
import os


async def ejecutar(user):
    """
    Gets the number of games a Steam user owns.

    Args:
        user: The SteamID of the user to get the number of games for.

    Returns:
        The number of games owned by the user if the request
        is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")
    steamid = user

    url = (
        f"https://api.steampowered.com/IPlayerService/GetOwnedGames"
        f"/v0001/?key={api_key}&steamid={steamid}&format=json"
    )

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            iddd = data["response"]["game_count"]
        else:
            print(f"Error retrieving data: {response.status}")
            iddd = None
    return iddd

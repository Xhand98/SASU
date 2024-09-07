import aiohttp
import os


async def ejecutar(user):
    api_key = os.getenv("STEAM_API_KEY")
    steamid = user

    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steamid}&format=json"

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            iddd = data["response"]["game_count"]
        else:
            print(f"Error retrieving data: {response.status}")
            iddd = None
    return iddd

import aiohttp
import os


async def ejecutar(user):
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = (f"https://api.steampowered.com/ISteamUser/Resolve"
           f"VanityURL/v0001/?key={api_key}&vanityurl={steamuser}")

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            iddd = data["response"]["steamid"]
            print(iddd)  # Optional: print SteamID for debugging
        else:
            print(f"Error retrieving data: {response.status}")
            iddd = None
    return iddd

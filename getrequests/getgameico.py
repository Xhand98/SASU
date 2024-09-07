import aiohttp
import os


async def ejecutar(user):
    api_key = os.getenv("STEAM_API_KEY")
    code = None

    url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={api_key}&steamid={user}"
    async with aiohttp.ClientSession() as session, session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if (
                    "response" in data
                    and "games" in data["response"]
                    and len(data["response"]["games"]) > 0
                ):
                    game = data["response"]["games"][-1]
                    appid = game["appid"]
                    code = game.get("img_icon_url", "default")
                    icourl = f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{code}.jpg"
                    print(icourl)
            else:
                print(f"Error al obtener los datos: {response.status}")
                icourl = None
    return icourl

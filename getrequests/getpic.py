import aiohttp
import os


async def ejecutar(user):
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={user}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                iddd = data["response"]["players"][0]["avatarfull"]
            else:
                print(f"Error al obtener los datos: {response.status}")
                iddd = None
    return iddd


async def personaname(user):
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={user}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                info = data["response"]["players"][0]["personaname"]
            else:
                print(f"Error al obtener los datos: {response.status}")
                info = None
    return info


async def link(user):
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={user}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                info = data["response"]["players"][0]["profileurl"]
            else:
                print(f"Error al obtener los datos: {response.status}")
                info = None
    return info


async def get_country(user):
    api_key = os.getenv("STEAM_API_KEY")
    steamuser = user

    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamuser}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                players = data["response"]["players"]

                if len(players) > 0 and "loccountrycode" in players[0]:
                    country_code = players[0]["loccountrycode"]

                    def country_code_to_flag(country_code):
                        country_code = country_code.upper()
                        flag = "".join(
                            chr(0x1F1E6 + ord(char) - ord("A")) for char in country_code
                        )
                        return flag

                    flag = country_code_to_flag(country_code)
                else:
                    flag = "No flag/bandera"
            else:
                flag = f"Error retrieving data: {response.status}"
    return flag

import aiohttp
import os


async def ejecutar(user):
    """Fetches the avatar URL of a Steam user from their SteamID.

    Args:
        user: The SteamID of the user to fetch the avatar URL of.

    Returns:
        The avatar URL of the user, or None if an error occurred.
    """
    api_key = os.getenv("STEAM_API_KEY")

    url = (
        f"https://api.steampowered.com/ISteamUser/"
        f"GetPlayerSummaries/v0002/?key={api_key}&steamids={user}"
    )

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            iddd = data["response"]["players"][0]["avatarfull"]
        else:
            print(f"Error al obtener los datos: {response.status}")
            iddd = None
    return iddd


async def personaname(user):
    """Fetches the username of a Steam user from their SteamID.

    Args:
        user: The SteamID of the user to fetch the username of.

    Returns:
        The username of the user if the request is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")

    url = (
        f"https://api.steampowered.com/ISteamUser/GetPlayer"
        f"Summaries/v0002/?key={api_key}&steamids={user}"
    )

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            info = data["response"]["players"][0]["personaname"]
        else:
            print(f"Error al obtener los datos: {response.status}")
            info = None
    return info


async def link(user):
    """Fetches the profile URL of a Steam user from their SteamID.

    Args:
        user: The SteamID of the user to fetch the profile URL of.

    Returns:
        The profile URL of the user if the request is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")

    url = (
        f"https://api.steampowered.com/ISteamUser/"
        f"GetPlayerSummaries/v0002/?key={api_key}&steamids={user}"
    )

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            info = data["response"]["players"][0]["profileurl"]
        else:
            print(f"Error al obtener los datos: {response.status}")
            info = None
    return info


async def get_country(user):
    """Fetches the country code of a Steam user from their SteamID.

    Args:
        user: The SteamID of the user to fetch the country code of.

    Returns:
        The country code of the user if the request is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")

    url = (
        f"https://api.steampowered.com/ISteamUser/"
        f"GetPlayerSummaries/v0002/?key={api_key}&steamids={user}"
    )

    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            players = data["response"]["players"]
            if len(players) > 0 and "loccountrycode" in players[0]:
                country_code = players[0]["loccountrycode"]

                def country_code_to_flag(country_code):
                    """
                    Converts a country code (like "US" or "GB") to an emoji flag.

                    Args:
                        country_code: The country code to convert.

                    Returns:
                        The country code as an emoji flag,
                        or None if the country code is not valid.
                    """
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

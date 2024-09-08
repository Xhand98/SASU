import httpx
import os

# Create a single AsyncClient instance
client = httpx.AsyncClient()


async def fetch_data(url, params=None):
    """
    Fetches JSON data from a given Steam Web API URL.

    Args:
        url: The URL of the Steam Web API to fetch data from.
        params: Optional parameters to include in the request.

    Returns:
        The JSON data returned by the API endpoint.

    Raises:
        httpx.HTTPStatusError: If the response was unsuccessful.
    """
    response = await client.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


async def get_hours(user):
    """
    Gets the total hours a user has played across all of their games.

    Args:
        user: The SteamID of the user to get the total hours for.

    Returns:
        The total hours played by the user, or 0 if the response is unsuccessful.
    """
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": api_key,
        "steamid": user,
        "include_appinfo": 1,
        "include_played_free_games": 1,
    }

    data = await fetch_data(url, params=params)
    total_hours = sum(
        game.get("playtime_forever", 0) / 60
        for game in data.get("response", {}).get("games", [])
    )
    return total_hours


async def get_steamid(user):
    """
    Resolve a Steam vanity URL to a SteamID.

    Args:
        user: The vanity URL of the user to resolve.

    Returns:
        The SteamID of the resolved user, or None if an error occurred.
    """
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {"key": api_key, "vanityurl": user}

    data = await fetch_data(url, params=params)
    return data.get("response", {}).get("steamid")


async def get_games(user):
    """
    Gets the number of games a user owns.

    Args:
        user: The SteamID of the user to get the number of games for.

    Returns:
        The number of games the user owns, or 0 if an error occurred.
    """
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {"key": api_key, "steamid": user, "include_appinfo": 1}

    data = await fetch_data(url, params=params)
    return len(data.get("response", {}).get("games", []))


async def get_pic(user):
    """
    Fetches the avatar URL, profile URL, and username of
    a Steam user from their SteamID.

    Args:
        user: The SteamID of the user to fetch the info of.

    Returns:
        A dictionary containing the avatar URL, profile URL,
        and username of the user if the request is successful,
        otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?"
    params = {"key": api_key, "steamids": user}

    data = await fetch_data(url, params=params)
    players = data.get("response", {}).get("players", [])
    if players:
        player = players[0]
        return {
            "avatar": player.get("avatarfull"),
            "profileurl": player.get("profileurl"),
            "personaname": player.get("personaname"),
        }

    return None


async def get_level(user):
    """
    Gets the level of a Steam user.

    Args:
        user: The SteamID of the user to get the level of.

    Returns:
        The level of the user if the request is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/IPlayerService/GetBadges/v1/"
    params = {"key": api_key, "steamid": user}

    data = await fetch_data(url, params=params)
    return data.get("response", {}).get("player_level")


async def get_badges(user):
    """
    Gets the number of Steam badges a user has.

    Args:
        user: The SteamID of the user to get the number of badges for.

    Returns:
        The number of badges the user has, or 0 if an error occurred.
    """
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/IPlayerService/GetBadges/v1/"
    params = {"key": api_key, "steamid": user}

    data = await fetch_data(url, params=params)
    return len(data.get("response", {}).get("badges", []))


async def get_country(user):
    """
    Fetches the country code of a Steam user from their SteamID.

    Args:
        user: The SteamID of the user to fetch the country code of.

    Returns:
        The country code of the user if the request is successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {"key": api_key, "steamids": user}

    data = await fetch_data(url, params=params)
    player = data.get("response", {}).get("players", [{}])[0]
    country_code = player.get("loccountrycode", "")

    def country_code_to_flag(cc):
        """
        Converts a country code (like "US" or "GB") to an emoji flag.

        Args:
            cc: The country code to convert.

        Returns:
            The country code as an emoji flag, or None if the country code is not valid.
        """
        code = cc.upper()
        return "".join(chr(0x1F1E6 + ord(char) - ord("A")) for char in code)

    return country_code_to_flag(country_code) if country_code else "No flag/bandera"


# Close the client when the application shuts down
async def close_client():
    """
    Closes the aiohttp client session when the application is shutting down.

    This is a necessary step to prevent the application from leaking resources.
    """
    await client.aclose()

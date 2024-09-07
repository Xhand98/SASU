import httpx
import os

# Create a single AsyncClient instance
client = httpx.AsyncClient()


async def fetch_data(url, params=None):
    response = await client.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


async def get_hours(user):
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
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    params = {"key": api_key, "vanityurl": user}

    data = await fetch_data(url, params=params)
    return data.get("response", {}).get("steamid")


async def get_games(user):
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {"key": api_key, "steamid": user, "include_appinfo": 1}

    data = await fetch_data(url, params=params)
    return len(data.get("response", {}).get("games", []))


async def get_pic(user):
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
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/IPlayerService/GetBadges/v1/"
    params = {"key": api_key, "steamid": user}

    data = await fetch_data(url, params=params)
    return data.get("response", {}).get("player_level")


async def get_badges(user):
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/IPlayerService/GetBadges/v1/"
    params = {"key": api_key, "steamid": user}

    data = await fetch_data(url, params=params)
    return len(data.get("response", {}).get("badges", []))


async def get_country(user):
    api_key = os.getenv("STEAM_API_KEY")
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {"key": api_key, "steamids": user}

    data = await fetch_data(url, params=params)
    player = data.get("response", {}).get("players", [{}])[0]
    country_code = player.get("loccountrycode", "")

    def country_code_to_flag(country_code):
        country_code = country_code.upper()
        return "".join(chr(0x1F1E6 + ord(char) - ord("A")) for char in country_code)

    return country_code_to_flag(country_code) if country_code else "No flag/bandera"


# Close the client when the application shuts down
async def close_client():
    await client.aclose()

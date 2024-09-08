import aiohttp
import asyncio
import os

from dotenv import load_dotenv

# CONFIG
load_dotenv()
API_KEY = os.getenv("STEAM_API_KEY")


# Helper function to fetch JSON data
async def fetch_json(session, url):
    """Fetches JSON data from the given URL using the given session.

    Args:
        session: The aiohttp.ClientSession to use for the request.
        url: The URL of the JSON data to fetch.

    Returns:
        The JSON data returned by the API endpoint.

    Raises:
        ValueError: If the response body is not valid JSON.
    """
    
    async with session.get(url) as response:
        try:
            data = await response.json()
            return data
        except aiohttp.ContentTypeError as e:
            error_body = await response.text()
            raise ValueError(f"Invalid response body: {error_body, e}")


# Get Achievements
async def get_achievements(session, app_id, steam_id, api):
    """Fetches the achievements of a user for a specific game.

    Args:
        session: The aiohttp.ClientSession to use for the request.
        app_id: The Steam App ID of the game to fetch achievements for.
        steam_id: The Steam ID of the user to fetch achievements for.
        api: The Steam Web API key to use for the request.

    Returns:
        The JSON data returned by the API endpoint.

    Raises:
        ValueError: If the response body is not valid JSON.
    """
    
    url = (f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
           f"?appid={app_id}"
           f"&key={api}"
           f"&steamid={steam_id}")
    json_res = await fetch_json(session, url)
    return json_res


# Get Player Games
async def get_player_games(session, steam_id):
    """Fetches the games of a user and their unlocked achievements.

    Args:
        session: The aiohttp.ClientSession to use for the request.
        steam_id: The Steam ID of the user to fetch games and achievements for.

    Returns:
        The total number of unlocked achievements across all games.
    """
    
    url = (f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
           f"?key={API_KEY}"
           f"&steamid={steam_id}"
           f"&format=json"
           f"&include_appinfo=1"
           f"&include_played_free_games=1")
    json_res = (await fetch_json(session, url))["response"]

    unlocked_achievement_count = 0

    # Concurrently fetch achievements for all games
    tasks = []
    for game in json_res.get("games", []):
        tasks.append(fetch_achievements_for_game(session, game["appid"], steam_id))

    results = await asyncio.gather(*tasks)

    # Process results
    for unlocked_achievements in results:
        unlocked_achievement_count += len(unlocked_achievements)

    return unlocked_achievement_count


# Helper function to fetch achievements for a specific game
async def fetch_achievements_for_game(session, app_id, steam_id):
    """Fetches the unlocked achievements for a specific game of a user.

    Args:
        session: The aiohttp.ClientSession to use for the request.
        app_id: The Steam App ID of the game to fetch achievements for.
        steam_id: The Steam ID of the user to fetch achievements for.

    Returns:
        A list of the unlocked achievements for the game.

    Raises:
        ValueError: If the response body is not valid JSON.
    """
    
    achievements = await get_achievements(session, app_id, steam_id, API_KEY)
    print(f"Game {app_id}: {achievements}")  # Debugging line
    if "playerstats" in achievements and "achievements" in achievements["playerstats"]:
        return [
            ac
            for ac in achievements["playerstats"]["achievements"]
            if ac["achieved"] != 0
        ]
    return []


# Processing Data
async def process_data(session, steam_id):
    """Fetches the number of unlocked achievements of a user.

    Args:
        session: The aiohttp.ClientSession to use for the request.
        steam_id: The Steam ID of the user to fetch achievements for.

    Returns:
        The number of unlocked achievements of the user if the request is successful,
        otherwise a string with an error message.

    Raises:
        ValueError: If the response body is not valid JSON.
    """

    try:
        unlocked_achievement_count = await get_player_games(session, steam_id)
        if unlocked_achievement_count == 0:
            return "Couldn't find your achievements."
        return unlocked_achievement_count
    except Exception as err:
        return f"Error: {err}"


# Example usage
async def main(steam_id):
    """Example usage of the getachievements module.

    This function demonstrates how to use the 
    getachievements module to fetch the
    number of unlocked achievements of a Steam user.

    Args:
        steam_id: The Steam ID of the user to fetch achievements for.

    Returns:
        The number of unlocked achievements of 
        the user if the request is successful,
        otherwise a string with an error message.
    """
    async with aiohttp.ClientSession() as session:
        result = await process_data(session, steam_id)
        print(result)
    return result

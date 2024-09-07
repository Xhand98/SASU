import aiohttp
import asyncio
import os

from dotenv import load_dotenv

# CONFIG
load_dotenv()
API_KEY = os.getenv("STEAM_API_KEY")


# Helper function to fetch JSON data
async def fetch_json(session, url):
    async with session.get(url) as response:
        try:
            data = await response.json()
            return data
        except aiohttp.ContentTypeError as e:
            error_body = await response.text()
            raise ValueError(f"Invalid response body: {error_body, e}")


# Get Achievements
async def get_achievements(session, app_id, steam_id, api):
    url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={api}&steamid={steam_id}"
    json_res = await fetch_json(session, url)
    return json_res


# Get Player Games
async def get_player_games(session, steam_id):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={steam_id}&format=json&include_appinfo=1&include_played_free_games=1"
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
    try:
        unlocked_achievement_count = await get_player_games(session, steam_id)
        if unlocked_achievement_count == 0:
            return "Couldn't find your achievements."
        return unlocked_achievement_count
    except Exception as err:
        return f"Error: {err}"


# Example usage
async def main(steam_id):
    async with aiohttp.ClientSession() as session:
        result = await process_data(session, steam_id)
        print(result)
    return result

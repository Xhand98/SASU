import aiohttp
import asyncio

# CONFIG
API_KEY = '51DD19FC173EFB74D9D7E09C6A61DDCE'

# Create a single session instance
session = aiohttp.ClientSession()

# Helper function to fetch JSON data
async def fetch_json(url):
    async with session.get(url) as response:
        try:
            data = await response.json()
            return data
        except aiohttp.ContentTypeError as e:
            error_body = await response.text()
            raise ValueError(f"Invalid response body: {error_body}")

# Get Achievements
async def get_achievements(app_id, steam_id):
    url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={app_id}&key={API_KEY}&steamid={steam_id}"
    json_res = await fetch_json(url)
    return json_res

# Get Player Games
async def get_player_games(steam_id):
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={steam_id}&format=json&include_appinfo=1&include_played_free_games=1"
    json_res = (await fetch_json(url))['response']
    
    unlocked_achievement_count = 0

    # Concurrently fetch achievements for all games
    tasks = []
    for game in json_res['games']:
        tasks.append(fetch_achievements_for_game(game['appid'], steam_id))
    
    results = await asyncio.gather(*tasks)

    # Process results
    for unlocked_achievements in results:
        unlocked_achievement_count += len(unlocked_achievements)
    
    return unlocked_achievement_count

# Helper function to fetch achievements for a specific game
async def fetch_achievements_for_game(app_id, steam_id):
    achievements = await get_achievements(app_id, steam_id)
    if 'playerstats' in achievements and 'achievements' in achievements['playerstats']:
        return [ac for ac in achievements['playerstats']['achievements'] if ac['achieved'] != 0]
    return []

# Processing Data
async def process_data(steam_id):
    try:
        unlocked_achievement_count = await get_player_games(steam_id)
        return f'Achievements unlocked: {unlocked_achievement_count}'
    except Exception as err:
        return f"Error: {err}"

# Close the session when done
async def close_session():
    await session.close()

# Example usage
async def main(steam_id):
    result = await process_data(steam_id)
    print(result)
    await close_session()

# Replace 'your_steam_id' with actual Steam ID
# asyncio.run(main('your_steam_id'))

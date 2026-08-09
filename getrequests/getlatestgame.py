from typing import List

import aiohttp
import os
from pydantic import BaseModel, Field

class GameShort(BaseModel):
    appid: int
    name: str
    playtime_2weeks: int
    playtime_forever: int
    icon_url: str | None = Field(
        default=None,
        alias="img_icon_url",
    )
class ResponseContainer(BaseModel):
    total_count: int = 0
    games: List[GameShort] = Field(default_factory=list)

class CompactSteamResponse(BaseModel):
    response: ResponseContainer


async def ejecutar(user: str) -> GameShort | None:
    """
    Gets the icon URL of the last game played by a Steam user.

    Args:
        user: The SteamID of the user to get the last game played of.

    Returns:
        The icon URL of the last game played
        by the user if the request is
        successful, otherwise None.
    """
    api_key = os.getenv("STEAM_API_KEY")

    url = (
        f"https://api.steampowered.com/IPlayerService/"
        f"GetRecentlyPlayedGames/v1/"
    )
    params = {
        "key": api_key,
        "steamid": user,
        "format": "json",
    }
    
    timeout = aiohttp.ClientTimeout(total=15)
    
    try:
        async with aiohttp.ClientSession(
            timeout=timeout,
            headers={
                "User-Agent": "SteamAchievemetsShowUp/1.0",
                "Accept": "application/json",},) as session:
                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        print(f"Error al obtener los datos: {response.status}")
                        return None
                    raw = await response.read()
        
        import json
        data = json.loads(raw)
        
        steam_response: CompactSteamResponse = CompactSteamResponse.model_validate(data)
    
    except aiohttp.ClientError as e:
        print(f"Steam connection error: {type(e).__name__}: {e}")
        return None

    except json.JSONDecodeError as e:
        print(f"Steam returned invalid JSON: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        return None

        
        
        
    if not steam_response.response.games:
        return None
        
    return steam_response.response.games[-1]

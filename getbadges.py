import requests
import os

def get_levels(user):
    api_key = os.environ['STEAM_API_KEY']
    
    steamuser = user

    # URL de la API de Steam para obtener la lista de juegos que posees y las horas jugadas
    url = f'https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={api_key}&steamid={steamuser}&skip_unvetted_apps=0&include_appinfo=1&include_played_free_games=1&include_free_sub=1'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        info = data['response']['player_level']
    else:
        print(f'Error al obtener los datos: {response.status_code}')
        json_data = None
    return info

def get_badges(user):
    api_key = os.environ['STEAM_API_KEY']

    steamuser = user

    # URL de la API de Steam para obtener la lista de juegos que posees y las horas jugadas
    url = f'https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={api_key}&steamid={steamuser}&skip_unvetted_apps=0&include_appinfo=1&include_played_free_games=1&include_free_sub=1'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        info = len(data['response']['badges'])
    else:
        print(f'Error al obtener los datos: {response.status_code}')
        json_data = None
    return info
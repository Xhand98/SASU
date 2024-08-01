import requests
import os

def ejecutar(user):

    api_key = os.environ['STEAM_API_KEY'] 
    steamuser = user

    url = f'https://api.steampowered.com/IPlayerService/GetBadges/v1/?key={api_key}&steamid={user}&skip_unvetted_apps=0'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        info = data['response']['player_level'] 
    else:
        print(f'Error al obtener los datos: {response.status_code}')
    return info
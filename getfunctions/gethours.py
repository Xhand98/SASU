import requests
import os

def ejecutar(user):

    api_key = os.environ['STEAM_API_KEY']
    steam_id = user

    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        total_playtime_minutes = sum(game['playtime_forever'] for game in data['response']['games'])
        total_playtime_hours = total_playtime_minutes / 60
        print(f'Has jugado un total de {total_playtime_hours:.2f} horas en Steam.')
        user = f'{total_playtime_hours:.2f} hours'
    else:
        print(f'Error al obtener los datos: {response.status_code}')

    return user

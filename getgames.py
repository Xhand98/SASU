import requests
import os


def ejecutar(user):

    api_key = os.environ['STEAM_API_KEY']  # Tu SteamID
    steamuser = user

    # URL de la API de Steam para obtener la lista de juegos que posees y las horas jugadas
    url = f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={user}&format=json'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        iddd = data['response']['game_count']
    else:
        print(f'Error al obtener los datos: {response.status_code}')
    return iddd

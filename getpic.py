import requests
import os


def ejecutar(user):

    api_key = os.environ['STEAM_API_KEY']  # Tu SteamID
    steamuser = user

    # URL de la API de Steam para obtener la lista de juegos que posees y las horas jugadas
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={user}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        iddd = data['response']['players']['avatar_full']
    else:
        print(f'Error al obtener los datos: {response.status_code}')
    return iddd

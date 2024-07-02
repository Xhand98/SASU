import requests
import dotenv
import os

def ejecutar():
    dotenv.load_dotenv()

    api_key = '51DD19FC173EFB74D9D7E09C6A61DDCE'

    # Tu SteamID
    steam_id = '76561198930935250'

    # URL de la API de Steam para obtener la lista de juegos que posees y las horas jugadas
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        total_playtime_minutes = sum(game['playtime_forever'] for game in data['response']['games'])
        total_playtime_hours = total_playtime_minutes / 60
       ## print(f'Has jugado un total de {total_playtime_hours:.2f} horas en Steam.')
        result = f'Has jugado un total de {total_playtime_hours:.2f} horas en Steam'
    else:
        print(f'Error al obtener los datos: {response.status_code}')
    return result

hours = ejecutar()
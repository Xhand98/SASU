from replit import info
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
        iddd = data['response']['players'][0]['avatarfull']
    else:
        print(f'Error al obtener los datos: {response.status_code}')
    return iddd

def personaname(user):
    api_key = os.environ['STEAM_API_KEY']  # Tu SteamID
    steamuser = user

    # URL de la API de Steam para obtener la lista de juegos que posees y las horas jugadas
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={user}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        info = data['response']['players'][0]['personaname']
    else:
        print(f'Error al obtener los datos: {response.status_code}')
    return info

def link(user):
    api_key = os.environ['STEAM_API_KEY']  # Tu SteamID
    steamuser = user

    # URL de la API de Steam para obtener la lista de juegos que posees y las horas jugadas
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={user}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        info = data['response']['players'][0]['profileurl']
    else:
        print(f'Error al obtener los datos: {response.status_code}')
    return info


def get_country(user):
    api_key = os.environ['STEAM_API_KEY']
    steamuser = user

    # URL de la API de Steam para obtener la lista de juegos que posees y las horas jugadas
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamuser}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        players = data['response']['players']

        if len(players) > 0 and 'loccountrycode' in players[0]:
            country_code = players[0]['loccountrycode']

            def country_code_to_flag(country_code):
                # Convert the country code to uppercase
                country_code = country_code.upper()

                # Convert each letter to its corresponding regional indicator symbol
                flag = ''.join(chr(0x1F1E6 + ord(char) - ord('A')) for char in country_code)

                return flag

            flag = country_code_to_flag(country_code)
        else:
            flag = 'No flag/bandera'
    else:
        flag = f'Error retrieving data: {response.status_code}'

    return flag
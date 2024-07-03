import os
import discord
import requests
import json
from replit import db
import gethours
import getsteamid
import embed
import datetime
import getgames

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def get_steamid(steamid):
  steamid = getsteamid.ejecutar(steamid)
  return steamid


def get_steamh(res):
  res = gethours.ejecutar(res)
  return res

def get_steamg(ans):
  ans = getgames.ejecutar(ans)
  return ans


def get_cfact():
  response = requests.get('https://catfact.ninja/fact')
  json_data = json.loads(response.text)
  cfact = '> ' + json_data['fact']
  return cfact


def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  author = ' ***-' + json_data[0]['a'] + '***'
  quote = '> ' + json_data[0]['q'] + author
  return quote


def get_user(content):
  _, username = content.split(' ', 1)
  return username


def process_user_or_steamid(user_input):
  if user_input.isdigit() and len(user_input) == 17:
    return user_input  # SteamID
  else:
    return get_steamid(user_input)  # Username


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!quote'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('!cfact'):
    cfact = get_cfact()
    await message.channel.send(cfact)

  if message.content.startswith('!steamhours'):
    steamhresult = get_steamh('76561198930935250')
    await message.channel.send(steamhresult)

  if message.content.startswith('kys'):
    await message.channel.send(
        f'Ill make sure to Kiss Myself very well :D {message.author}')

  if message.content.startswith('!getuserid'):
    user_message = get_user(message.content)
    steamid = process_user_or_steamid(user_message)
    await message.channel.send(steamid)

  if message.content.startswith('!gethours'):
    user_message = get_user(message.content)
    steamid = process_user_or_steamid(user_message)
    steamhresult = get_steamh(steamid)
    await message.channel.send(steamhresult)

  if message.content.startswith('!embed'):
    user_message = get_user(message.content)
    steamid = process_user_or_steamid(user_message)
    steamhresult = get_steamh(steamid)
    user_games = get_steamg(steamid)
    coso = embed.create_embed(
        'User info',
        None,
        discord.Color.dark_gold(),
        (message.author.display_name, message.author.avatar),
        (f'More info coming soon...', None),
        [
            (
                'Total hours:', 
                f'{steamhresult}', 
                True
            ),
            (
                'Total games:', 
               f'{user_games}' + ' games', 
                True
            ),
            (
                'Total achievements unlocked:',
                'db_user_data[2]',
                True
            ),
            (
                '\u200B',
                '\u200B',
                False  
            ),
            (
                'Server Stats', 
                '', 
                False, 
                [
                    (
                        'Tournaments participated:', 
                        'db_server_data[0]', 
                        True
                    ),
                    (
                        'Tournaments won:', 
                        'db_server_data[1]', 
                        True
                    ),
                    (
                        'Server Achievements:', 
                        'Coming soon...', 
                        True
                    )
                ]
            ),
            (
                '\u200B',
                '\u200B',
                False
            )
        ]
    )
    await message.channel.send(embed=coso)

  if message.content.startswith('!getgames'):
    user_message = get_user(message.content)
    steamid = process_user_or_steamid(user_message)
    user_games = get_steamg(steamid)
  await message.channel.send(user_games)
  
client.run(os.environ['TOKEN'])

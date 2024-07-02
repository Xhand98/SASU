import os
import discord
import requests
import json
from replit import db
import gethours
import getsteamid

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def get_steamid(steamid):
  steamid = getsteamid.ejecutar(steamid)
  return steamid


def get_steamh():
  steamhresult = gethours.ejecutar()
  return steamhresult


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
    steamhresult = get_steamh()
    await message.channel.send(steamhresult)

  if message.content.startswith('kys'):
    await message.channel.send(
        f'Ill make sure to Kiss Myself very well :D {message.author.mention}')

  if message.content.startswith('!getuser'):
    user_message = get_user(message.content)
    steamid = get_steamid(user_message)
    print(steamid)
    await message.channel.send(steamid)


client.run(os.environ['TOKEN'])

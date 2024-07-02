import os
import discord
import requests
import json
import gethours



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_steamh():
  steamhresult = gethours.ejecutar()
  result = gethours.hours
  return result


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
    steamhresults = get_steamh()
    await message.channel.send(steamhresults)

  if message.content.startswith('kys'):
    await message.channel.send('Ill make sure to Kiss Myself very well :D')


client.run(os.environ['TOKEN'])

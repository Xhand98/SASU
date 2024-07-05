import datetime
import json
import os

import discord
import requests

from getfunctions.getbadges import get_badges as getbadges
from getfunctions.getbadges import get_levels as getlevels
from getfunctions.getgames import ejecutar as getgames
from getfunctions.gethours import ejecutar as gethours
from getfunctions.getpic import get_country as getcountry
from getfunctions.getpic import ejecutar as getpic
from getfunctions.getpic import link as getlink
from getfunctions.getpic import personaname as getpersonaname
from getfunctions.getsteamid import ejecutar as getsteamid

from replit import db

import embed



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def get_steamid(steamid):
    steamid = getsteamid(steamid)
    return steamid


def get_steamh(res):
    res = gethours(res)
    return res


def get_steamg(ans):
    ans = getgames(ans)
    return ans


def get_steampfp(pfp):
    pfp = getpic(pfp)
    return pfp

def get_steamname(pfp):
  pfp = getpersonaname(pfp)
  return pfp

def get_steamlink(pfp):
  pfp = getlink(pfp)
  return pfp

def get_steamlevels(pfp):
  level  = getlevels(pfp)
  return level

def get_steambadges(pfp):
  level  = getbadges(pfp)
  return level

def get_steamcountry(pfp):
  country  = getcountry(pfp)
  return country

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

    if message.content.startswith('!getuser'):
        user_message = get_user(message.content)
        steamid = process_user_or_steamid(user_message)
        steamhresult = get_steamh(steamid)
        user_games = get_steamg(steamid)
        user_pfp = get_steampfp(steamid)
        user_name = get_steamname(steamid)
        user_link = get_steamlink(steamid)
        level = get_steamlevels(steamid)
        badges = get_steambadges(steamid)
        country = get_steamcountry(steamid)
        coso = embed.create_embed(
            'User info',
            'Preview of a users profile',
            discord.Color.from_rgb(27,40,56),
            (user_name, user_pfp),
            (f'Steam link: {user_link}', user_pfp),
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
                    'User level:',
                    f'{level}',
                    True
                ),
                (
                    '\u200B',
                    '\u200B',
                    False
                ),
                (
                    'Other info',
                    '',
                    False,
                    [
                        (
                            'User badges:',
                            f'{badges}',
                            True
                        ),
                        (
                            'User country:',
                            f'{country}',
                            True
                        ),
                        (
                            'Achievements:',
                            'Coming soon...',
                            True
                        )
                    ]
                ),
                (
                    '\u200B',
                    '\u200B',
                    True
                )
            ]
        )
        await message.channel.send(embed=coso)

    if message.content.startswith('!getgames'):
      user_message = get_user(message.content)
      steamid = process_user_or_steamid(user_message)
      user_games = get_steamg(steamid)
      await message.channel.send(user_games)


    if message.content.startswith('!getpfp'):
      user_message = get_user(message.content)
      steamid = process_user_or_steamid(user_message)
      user_pfp = get_steampfp(steamid)
      await message.channel.send(user_pfp)


    if message.content.startswith('!getlink'):
      user_message = get_user(message.content)
      steamid = process_user_or_steamid(user_message)
      user_link = get_steamlink(steamid)
      await message.channel.send(user_link)

    if message.content.startswith('!getlevel'):
      user_message = get_user(message.content)
      steamid = process_user_or_steamid(user_message)
      level = get_steamlevels(steamid)
      await message.channel.send(level)

    if message.content.startswith('!getbadges'):
      user_message = get_user(message.content)
      steamid = process_user_or_steamid(user_message)
      badges = get_steambadges(steamid)
      await message.channel.send(badges)


    if message.content.startswith('!getcountry'):
      user_message = get_user(message.content)
      steamid = process_user_or_steamid(user_message)
      country = get_steamcountry(steamid)
      await message.channel.send(country)

client.run(os.environ['TOKEN'])

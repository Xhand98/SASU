from peewee import TextField
from .base import BaseModel

class DiscordUser(BaseModel):
    discord_id = TextField(unique=True, null=False)
    username = TextField(null=False)

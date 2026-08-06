from .base import BaseModel
from .discord_user import DiscordUser
from peewee import TextField, ForeignKeyField

class SteamAccount(BaseModel):
    id = TextField(unique=True, null=False)
    discord_id = ForeignKeyField(DiscordUser, backref='id', null=False)
    username = TextField(unique=False, null=False)

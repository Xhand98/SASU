import datetime
from peewee import ForeignKeyField, DateTimeField
from .base import BaseModel
from .discord_user import DiscordUser


class Blacklist(BaseModel):
    discord_id = ForeignKeyField(DiscordUser, backref='id')
    banned_at = DateTimeField(default=datetime.datetime.now)

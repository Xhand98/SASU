import datetime
from peewee import ForeignKeyField, DateTimeField
from .base import BaseModel
from .discord_user import DiscordUser


class Blacklist(BaseModel):
    discord = ForeignKeyField(DiscordUser, unique=True, backref='blacklist', on_delete='CASCADE')
    banned_at = DateTimeField(default=datetime.datetime.now)

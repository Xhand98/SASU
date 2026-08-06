from .base import BaseModel
from .discord_user import DiscordUser
from peewee import TextField, ForeignKeyField

class SteamAccount(BaseModel):
    steam_id = TextField(unique=True, null=False)
    discord = ForeignKeyField(
        DiscordUser,
        backref="steam_accounts",
        null=False,
        unique=True,
        on_delete="CASCADE",
    )
    username = TextField(unique=False, null=False)

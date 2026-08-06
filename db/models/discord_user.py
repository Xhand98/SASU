from peewee import TextField
from .base import BaseModel

class DiscordUser(BaseModel):
    id = TextField(unique=True, null=False),
    username = TextField(null=False)

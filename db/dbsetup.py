from db.database import db
from db.models import DiscordUser, SteamAccount, Blacklist

def setup_db():
    with db:
        db.create_tables([DiscordUser, SteamAccount, Blacklist])
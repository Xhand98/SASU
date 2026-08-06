from peewee import Model
from db.database import db

class BaseModel(Model):
    class Meta:
        database = db
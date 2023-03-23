import datetime

from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = db


class User(BaseModel):
    name = TextField(null=False)
    email = TextField(null=False, unique=True)
    password = TextField(null=False)
    token = TextField(null=True)


class Note(BaseModel):
    author = ForeignKeyField(User, null=False)
    title = TextField(null=False)
    text = TextField(null=False)
    edit_datetime = DateTimeField(default=datetime.datetime.now)
   
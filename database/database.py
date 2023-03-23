from .models import *


def create_tables():
    db.create_tables([
        User,
        Note
    ])

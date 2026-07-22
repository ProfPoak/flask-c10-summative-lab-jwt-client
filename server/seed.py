#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, User

fake = Faker()

with app.app_context():
    pass
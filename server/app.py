from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api, jwt
from models import User, UserSchema



if __name__ == '__main__':
    app.run(port=5555, debug=True)
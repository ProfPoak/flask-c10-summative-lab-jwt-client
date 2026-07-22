from flask import request, make_response, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity, jwt_required

from config import app, db, api, jwt
from models import User, UserSchema

class Signup(Resource):
    def post(self):
        try:
            json = request.get_json()
            user = User(
                username=json['username']
            )

            user.password_hash = json['password']

            db.session.add(user)
            db.session.commit()
        except (KeyError, ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 422

        access_token = create_access_token(identity=str(user.id))
        return make_response(
            jsonify(
                token=access_token, 
                user=UserSchema().dump(user)
            ),
            201
        )

class CheckSession(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return UserSchema().dump(user), 200
        
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
from flask import request, make_response, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime, timezone

from config import app, db, api, jwt
from models import User, UserSchema, JournalEntry, JournalEntrySchema

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
        user_id = int(get_jwt_identity())
        user = User.query.filter(User.id == user_id).first()
        return UserSchema().dump(user), 200

class Login(Resource):
   def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            access_token = create_access_token(identity=str(user.id))
            return make_response(
                        jsonify(
                            token=access_token, 
                            user=UserSchema().dump(user)
                        ),
                        200
                    )

        return {'error': 'Login failed. Please check Username and Password'}, 401

class Journal(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        user_id = int(get_jwt_identity())

        pagination = JournalEntry.query.filter_by(user_id=user_id)\
                .order_by(JournalEntry.date.desc())\
                .paginate(page=page, per_page=per_page, error_out=False)

        schema = JournalEntrySchema(many=True)

        return{
            'entries': schema.dump(pagination.items),
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total_pages': pagination.pages,
            'total_entries': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }, 200

    def post(self):
        user_id = int(get_jwt_identity())
        json = request.get_json()

        try:
            entry = JournalEntry(
                title=json['title'],
                date=datetime.now(timezone.utc),
                entry=json['entry'],
                user_id=user_id
            )

            db.session.add(entry)
            db.session.commit()
        except (KeyError, ValueError, IntegrityError) as e:
            db.session.rollback()
            return {'errors': [str(e)]}, 422

        return JournalEntrySchema().dump(entry), 201
        
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Journal, '/journal', endpoint='journal')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
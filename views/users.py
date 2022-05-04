from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from setup_db import db
from flask import request
from dao.model.user import User

from implemented import user_service

users_ns = Namespace('users')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_ns.route('/<int:user_id>')
class UsersView(Resource):
    def get(self, user_id):
        user = db.session.query(User).filter(User.id == user_id).first()

        if user is None:
            return {}, 404

        return user_schema.dump(user), 200

    def put(self, user_id):
        db.session.query(User).filter(User.id == user_id).update(request.json)
        db.session.commit()

        return None, 204

    def delete(self, user_id):
        db.session.query(User).filter(User.id == user_id).delete()
        db.session.commit()

        return None, 200


@users_ns.route('/')
class UsersView(Resource):
    def get(self):
        users = db.session.query(User).all()

        return users_schema.dump(users), 200

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return None, 201

from dao.auth import AuthDAO
from flask_restx import abort
from utils import get_hash, generate_tokens, decode_token


class AuthService:

    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def login(self, user_d: dict):
        user_data = self.dao.get_by_username(user_d['username'])
        if user_data is None:
            abort(401, message='user not found')

        hashed_pass = get_hash(user_d['password'])
        if user_data['password'] != hashed_pass:
            abort(401, message='invalid')

        tokens = generate_tokens(
            {
                'username': user_d['username'],
                'role': user_data['role']
            }
        )

        return tokens

    def get_new_tokens(self, refresh_token: str):

        decoded_token = decode_token(refresh_token, refresh_token=True)

        tokens = generate_tokens(
            user_d={
                'username': decoded_token['username'],
                'role': decoded_token['role']
            }
        )

        return tokens


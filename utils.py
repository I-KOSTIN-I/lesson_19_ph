import hashlib
from flask_restx import abort
import constants
import base64
from datetime import datetime, timedelta
import jwt
from flask import request, current_app
from dao.auth import AuthDAO
from typing import Dict



def get_hash(password: str) -> str:
    hash_pass = hashlib.pbkdf2_hmac(
        hash_name=constants.PWD_HASH_NAME,
        salt=constants.PWD_HASH_SALT.encode('utf-8'),
        iterations=constants.PWD_HASH_ITERATIONS,
        password=password.encode('utf-8')
    )

    return base64.b64encode(hash_pass).decode('utf-8')


def generate_tokens(user_d: dict) -> Dict[str, str]:
    user_d['exp'] = datetime.utcnow() + timedelta(minutes=30)
    user_d['refresh_token'] = False

    access_token = jwt.encode(
        payload=user_d,
        key=constants.SECRET_HERE,
        algorithm=constants.JWT_ALGORITHM
    )

    user_d['exp'] = datetime.utcnow() + timedelta(days=30)
    user_d['refresh_token'] = True

    refresh_token = jwt.encode(
        payload=user_d,
        key=constants.SECRET_HERE,
        algorithm=constants.JWT_ALGORITHM
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def get_token_from_headers(headers: dict):
    if 'Authorization' not in headers:
        abort(401)

    return headers['Authorization'].split(' ')[-1]


def decode_token(token: str, refresh_token: bool = False):

    decoded_token = {}

    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=constants.SECRET_HERE,
            algorithms=[constants.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        current_app.logger.info('Got wrong token: "%s"', token)
        abort(401)

    if decoded_token['refresh_token'] != refresh_token:
        abort(400, message='Got wrong token type')

    return decoded_token


def auth_required(func):
    def wrapper(*args, **kwargs):

        token = get_token_from_headers(request.headers)

        decoded_token = decode_token(token)

        if not AuthDAO.get_by_username(decoded_token['username']):
            abort(401)

        return func(*args, **kwargs)
    return wrapper


def admin_access_required(func):
    def wrapper(*args, **kwargs):

        token = get_token_from_headers(request.headers)

        decoded_token = decode_token(token)

        if decoded_token['role'] != 'admin':
            abort(403)

        if not AuthDAO.get_by_username(decoded_token['username']):
            abort(401)

        return func(*args, **kwargs)
    return wrapper






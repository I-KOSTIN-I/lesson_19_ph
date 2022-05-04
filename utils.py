import hashlib

import config
import constants
import base64
from datetime import datetime, timedelta
import jwt



def get_hash(password: str) -> str:
    hash_pass = hashlib.pbkdf2_hmac(
        hash_name=constants.PWD_HASH_NAME,
        salt=constants.PWD_HASH_SALT.encode('utf-8'),
        iterations=constants.PWD_HASH_ITERATIONS,
        password=password.encode('utf-8')
    )

    return base64.b64encode(hash_pass).decode('utf-8')


def generate_tokens(user_d):
    user_d['exp'] = datetime.utcnow() + timedelta(minutes=30)
    user_d['refresh_token'] = False

    access_token = jwt.encode(
        payload=user_d,
        key=config.SECRET_HERE,
        algorithm=constants.JWT_ALGORITHM
    )

    user_d['exp'] = datetime.utcnow() + timedelta(days=30)
    user_d['refresh_token'] = True

    refresh_token = jwt.encode(
        payload=user_d,
        key=config.SECRET_HERE,
        algorithm=constants.JWT_ALGORITHM
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }



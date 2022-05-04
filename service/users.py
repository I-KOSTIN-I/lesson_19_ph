from dao.user import UserDAO
from utils import get_hash


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create(self, user_d: dict) -> dict:
        user_d['password'] = get_hash(user_d['password'])
        self.dao.create(user_d)

        return user_d


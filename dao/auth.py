from dao.model.user import User


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def create(self, user_d):
        pass

    def get_by_username(self, username):
        user = self.session.query(User).filter(User.username == username).first()
        data = {
            "username": user.username,
            "role": user.role,
            "password": user.password
        }

        return data


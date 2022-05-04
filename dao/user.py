from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def create(self, user_d: dict) -> dict:
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

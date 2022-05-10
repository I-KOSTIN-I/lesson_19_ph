from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session
        
    def get_one(self, bid):
        return self.session.query(User).get(bid)
    
    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d: dict) -> dict:
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).all()

    def delete(self, bid):
        user = self.get_one(bid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.name = user_d.get("name")
        user.password = user_d.get("password")
        user.role = user_d.get("role")
        self.session.add(user)
        self.session.commit()

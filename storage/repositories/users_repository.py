from storage.db import User

class UsersRepository:
    def __init__(self, db):
        self.db = db

    def get_by_email(self, email):
        sess = self.db.get_session()
        return sess.query(User).filter_by(email=email).first()


    def add(self, data):
        sess = self.db.get_session()
        existing_user = sess.query(User).filter_by(email=data['email']).first()

        if not existing_user:
            user = User(email=data['email'], hashed_password=data['hashed_password'], salt=data['salt'])
            sess.add(user)
            sess.commit()
            sess.close()
            return True
        else:
            sess.close()
            return False
            

    def close(self):
        self.db.close()
from storage.db import Users

class UsersRepository:
    def __init__(self, db):
        self.db = db

    def get_by_email(self, email):

        return {'email': email, 'hash': '1231', 'salt': 'salt'}

    def close(self):
        self.db.close()
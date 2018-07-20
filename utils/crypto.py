import hashlib, uuid

def get_salt():
    return uuid.uuid4().hex


def generate_password_hash(password, salt):
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


def is_valid_password(password, hashed_password, salt):
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest() == hashed_password
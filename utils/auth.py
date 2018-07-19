#https://steelkiwi.com/blog/jwt-authorization-python-part-1-practise/
from datetime import datetime, timedelta
import jwt

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20

async def create_jwt_token(username):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

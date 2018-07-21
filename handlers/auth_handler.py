from aiohttp import web
from datetime import datetime, timedelta
from auth import crypto
from auth import auth
from auth.crypto import is_valid_password
import jwt
import json

async def login(request):
    try:
        data = await request.json()
        user = request.app.db.users_repository.get_by_email(data['email'])
        if user:
            if is_valid_password(data['password'], user.hashed_password, user.salt):
                jwt_token = await auth.create_jwt_token(data['email'])
                response_obj = { 'token': jwt_token.decode('utf-8') }
                return web.Response(text=json.dumps(response_obj), status=200)
        
        return web.Response(text='Unauthorized', status=401)
    except Exception as e:
        print(str(e))
        response_obj = { 'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=401)

async def signup(request):
    try:
        data = await request.json()
        
        salt = crypto.get_salt()
        hashed_password = crypto.generate_password_hash(data['password'], salt)

        result = request.app.db.users_repository.add({'email': data['email'], 'hashed_password': hashed_password, 'salt': salt})
        if not result:
            return web.Response(text='Error', status=500)
        
        response_obj = { 'status': 'success' }
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        print(str(e))
        response_obj = { 'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=401)
    

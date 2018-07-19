from aiohttp import web
from datetime import datetime, timedelta
from utils import auth
from utils.crypto import is_valid_password
import jwt
import json

async def login(request):
    try:
        data = await request.json()
        user = request.app.db.users_repository.get_by_email(data.email)
        if user:
            if is_valid_password(data.password, user.hash, user.salt):
                jwt_token = auth.create_jwt_token(data.email)
                response_obj = { 'token': jwt_token.decode('utf-8') }
                return web.Response(text=json.dumps(response_obj), status=200)
        
        return web.Response(text='Unauthorized', status=401)
    except Exception as e:
        print(str(e))
        response_obj = { 'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=401)
    

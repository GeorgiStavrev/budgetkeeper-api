import jwt
from utils import auth

async def get_user(request):
    return json_response({'user': str(request.user)})

async def auth_middleware(app, handler):
    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
            try:
                payload = await auth.decode_jwt_token(jwt_token)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return json_response({'message': 'Token is invalid'}, status=400)

            request.user = app.db.users_repository.get_by_email(payload['user_id'])
        return await handler(request)
    return middleware
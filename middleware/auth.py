import jwt
from auth import auth
from aiohttp import web

async def get_user(request):
    return web.json_response({'user': str(request.user)})

async def auth_middleware(app, handler):
    def has_permission(user, permission):
        return False

    async def middleware(request):
        request.user = None
        jwt_token = request.headers.get('authorization', None)
        if hasattr(handler, 'requires_authentication'):
            if jwt_token:
                try:
                    payload = await auth.decode_jwt_token(jwt_token)
                except (jwt.DecodeError, jwt.ExpiredSignatureError):
                    return web.json_response({'message': 'Token is invalid'}, status=400)
                
                user = app.db.users_repository.get_by_email(payload['user_id'])
                if hasattr(handler, 'permissions'):
                    missing_permissions = []
                    for p in handler.permissions:
                        if not has_permission(user, p):
                            missing_permissions.append(p)
                    
                    if len(missing_permissions) > 0:
                        return web.Response(text='Unauthorized: Missing permissions', status=401)

                request.user = user
            else:
                return web.Response(text='Unauthorized', status=401)

        return await handler(request)
    return middleware
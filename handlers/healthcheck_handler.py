from aiohttp import web

STATUS_OK = 'OK'

async def handle(request):
    data = {
        'api': STATUS_OK
    }
    return web.json_response(data=data, status=200)
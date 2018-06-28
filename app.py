from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', 'Anonymous')
    text = 'Hello, ' + name
    return web.Response(text=text)

app = web.Application()
routes = [web.get('/', handle), web.get('/{name}', handle)]
app.add_routes(routes)

web.run_app(app)
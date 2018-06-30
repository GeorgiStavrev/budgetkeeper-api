from aiohttp import web
import handlers.healthcheck_handler as healthcheck
import handlers.expenses_handler as expenses

async def handle(request):
    name = request.match_info.get('name', 'Anonymous')
    text = 'Hello, ' + name
    return web.Response(text=text)

app = web.Application()
app.router.add_get('/health', healthcheck.handle)
app.router.add_get('/expenses/monthly', expenses.get_monthly)
app.router.add_get('/expenses/today', expenses.get_today)

routes = [web.get('/', handle), web.get('/{name}', handle)]
app.add_routes(routes)


web.run_app(app)
from aiohttp import web
import handlers.healthcheck_handler as healthcheck
import handlers.expenses_handler as expenses

def setup_routes(app):
    # Health endpoint
    app.router.add_get('/health', healthcheck.handle)
    
    # Expenses endpoint
    app.router.add_get('/expenses/monthly', expenses.get_monthly)
    app.router.add_get('/expenses/today', expenses.get_today)
    app.router.add_get('/expenses/{id}', expenses.get)
    app.router.add_post('/expenses', expenses.post)
    app.router.add_put('/expenses/{id}', expenses.put)
    app.router.add_delete('/expenses/{id}', expenses.delete)
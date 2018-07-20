from aiohttp import web
import handlers.healthcheck_handler as healthcheck
import handlers.expenses_handler as expenses
import handlers.budgets_handler as budgets
import handlers.auth_handler as auth

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
    app.router.add_get('/budgets/{id}', budgets.get)
    app.router.add_post('/budgets', budgets.post)
    app.router.add_put('/budgets/{id}', budgets.put)
    app.router.add_delete('/budgets/{id}', budgets.delete)
    app.router.add_post('/auth/login', auth.login)
    app.router.add_post('/auth/signup', auth.signup)
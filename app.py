from aiohttp import web
import asyncpg, asyncpgsa
import asyncio
import handlers.healthcheck_handler as healthcheck
import handlers.expenses_handler as expenses
from middleware.error import error_middleware

from router import setup_routes
from config.app import default

from storage.db import StorageProvider, ExpensesRepository
import config.app.default as config

def bootstrap(loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    
    app = web.Application(loop=loop, middlewares=[error_middleware])
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    setup_routes(app)

    app.startup_exceptions = []

    return app

def _swallow_exceptions_set_startup_fail(f):
    async def wrapper(app):
        try:
            return await f(app)
        except Exception as e:
            app.startup_exceptions.append(e)
            #logging.exception("Exception during startup function '%s'", f.__name__)
    return wrapper

@_swallow_exceptions_set_startup_fail
async def init_pg(app):
    """Initialize Postgres engine."""
    print("Initializing database.")
    storage = StorageProvider(config.DATABASE, verbose=True)
    storage.set_up()
    storage.expenses_repository = ExpensesRepository(storage)
    print(storage)
    app.db = storage

async def close_pg(app):
    """Close connection to Postgres."""
    if hasattr(app, 'db'):
        await app.db.close()
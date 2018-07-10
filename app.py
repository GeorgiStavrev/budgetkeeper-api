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
import os

def bootstrap(loop=None):
    print("Bootstrapping the app.")
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
    print("Initializing database connection.")
    dbconfig = config.DATABASE
    dbconfig['host'] = os.environ['DBHOST'] if 'DBHOST' in os.environ else dbconfig['host']
    dbconfig['port'] = os.environ['DBPORT'] if 'DBPORT' in os.environ else dbconfig['port']
    dbconfig['password'] = os.environ['DBPASS'] if 'DBPASS' in os.environ else dbconfig['password']
    dbconfig['user'] = os.environ['DBUSER'] if 'DBUSER' in os.environ else dbconfig['user']
    dbconfig['database'] = os.environ['DBNAME'] if 'DBNAME' in os.environ else dbconfig['database']

    storage = StorageProvider(config.DATABASE, verbose=True)

    print("Initializing database schema.")
    storage.set_up()

    print("Initializing expenses repository.")
    storage.expenses_repository = ExpensesRepository(storage)
    app.db = storage

    print("Database initialized.")

async def close_pg(app):
    """Close connection to Postgres."""
    if hasattr(app, 'db'):
        await app.db.close()
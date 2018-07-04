from config.app.default import DATABASE
from storage.db import StorageProvider
import asyncio
import click

async def init_db(force=False):
    """Initialise DB with fake data"""
    storage = StorageProvider(config.DATABASE, verbose=True)
    storage.set_up()
    storage.expenses_repository = ExpensesRepository(storage)
    storage.close()


@click.command(help='Initialise Deals DB with fake data.')
@click.option('--force', '-f', is_flag=True, help='Force recreate.')
def command(force=False):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db(force=force))


if __name__ == '__main__':
    command()
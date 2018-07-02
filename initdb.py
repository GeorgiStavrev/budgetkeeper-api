from sqlalchemy.ext.declarative import declarative_base
from config.app.default import DATABASE
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

import asyncio
from models.expenses import expenses
import click
import os
import asyncpgsa

async def make_db_pool():
    host = os.environ.get('DB_HOST', 'localhost')
    return await asyncpgsa.create_pool(
        database=DATABASE['database'],
        host=host,
        max_size=3,
        min_size=1,
        port=DATABASE['port'],
        user=DATABASE['user'],
        password=DATABASE['password'],
    )

async def init_db(force=False):
    """Initialise DB with fake data"""
    pool = await make_db_pool()

    table_models = {
        'expenses': expenses
    }

    async with pool.acquire() as conn:
        for key,value in table_models.items():
            tables = await conn.fetch("SELECT * FROM information_schema.tables WHERE table_name = '{}'".format(key))
            if len(list(tables)) > 0 and not force:
                print('Table {} already exists. Exiting...'.format(key))
                return

    async with pool.acquire() as conn:
        for key,value in table_models.items():
            print('Dropping existing {} table...'.format(key))
            await conn.execute('DROP TABLE IF EXISTS {}'.format(key))
            print('Creating new {} table...'.format(key))
            await conn.fetch(str(CreateTable(value).compile(dialect=postgresql.dialect())))
    
   # print('Inserting fake data...')
   # values = itertools.chain(make_fake_data(2000), prepare_test_case_data(), prepare_limit_test_case_data())
   # coros = (insert_values(pool, deals, v) for v in chunk(values, 10))
   # tasks = [asyncio.ensure_future(coro) for coro in coros]

   # tasks += [asyncio.ensure_future(insert_values(pool, monthly_percentiles, list(make_monthly_percentiles())))]
   # await asyncio.wait(tasks)

@click.command(help='Initialise Deals DB with fake data.')
@click.option('--force', '-f', is_flag=True, help='Force recreate.')
def command(force=False):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db(force=force))


if __name__ == '__main__':
    command()
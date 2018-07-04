from aiohttp import web
from app import bootstrap

app = bootstrap()

if __name__ == "__main__":
    web.run_app(app)
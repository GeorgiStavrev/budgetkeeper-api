from aiohttp import web
from app import bootstrap

app = bootstrap()

if __name__ == "__main__":
    print("Starting app")
    web.run_app(app)
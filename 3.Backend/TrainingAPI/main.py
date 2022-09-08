import os

from sanic.response import text
from sanic_redis import SanicRedis

from app import create_app
from app.apis import api
from app.misc.log import log
from config import Config, LocalDBConfig

app = create_app(Config, LocalDBConfig)
redis = SanicRedis()

redis.init_app(app)

app.blueprint(api)


@app.route("/", methods={'GET', 'POST'})
async def hello_world(request):
    return text("Hello World")


if __name__ == '__main__':
    if 'SECRET_KEY' not in os.environ:
        log(message='SECRET KEY is not set in the environment variable.', keyword='WARN')
    app.run(**app.config['RUN_SETTING'])

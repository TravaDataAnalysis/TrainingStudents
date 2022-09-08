from sanic import Blueprint
from sanic.response import json

example = Blueprint('example_blueprint', url_prefix='/example')


@example.route('/')
async def bp_root(request):
    return json({'example': 'blueprint'})

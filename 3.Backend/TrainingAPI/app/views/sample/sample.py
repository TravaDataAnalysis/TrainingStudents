from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from app.decorators.json_validator import validate_with_jsonschema


class Sample(HTTPMethodView):
    @validate_with_jsonschema({
        'type': 'object',
        'required': ['age', 'name'],
        'properties': {
            'age': {
                'type': 'integer',
                'minimum': 0
            },
            'name': {
                'type': 'string'
            }
        }
    })
    async def post(self, request: Request):
        payload = request.json

        return json(payload, 201)

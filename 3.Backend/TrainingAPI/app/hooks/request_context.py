from sanic.request import Request
from sanic.response import HTTPResponse


async def after_request(request: Request, response: HTTPResponse) -> HTTPResponse:
    try:
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'deny'
    finally:
        return response

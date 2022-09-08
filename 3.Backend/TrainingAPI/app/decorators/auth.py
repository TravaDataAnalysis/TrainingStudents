from functools import wraps
import jwt

from config import Config
from app.hooks.error import ApiUnauthorized


def check_token(request):
    token = request.token
    if not token:
        return False, None

    try:
        jwt_ = jwt.decode(
            token, Config.SECRET_KEY, algorithms=["HS256"]
        )
        return True, jwt_
    except jwt.exceptions.InvalidTokenError:
        return False, None


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated, jwt_ = check_token(request)

            if is_authenticated:
                kwargs['username'] = jwt_['username']
                response = await f(request, *args, **kwargs)
                return response
            else:
                raise ApiUnauthorized("You are unauthorized.")

        return decorated_function

    return decorator(wrapped)

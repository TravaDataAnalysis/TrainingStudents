import datetime

import jwt

from config import Config


def generate_jwt(username, role='user'):
    expiration_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=Config.EXPIRATION_JWT)
    token = jwt.encode(
        {
            "username": username,
            "role": role,
            "exp": expiration_time
        }, 
        Config.SECRET_KEY
    )

    return token

from sanic import Blueprint
from sanic.response import json

from app.hooks.error import ApiInternalError
from app.utils.jwt_utils import generate_jwt
example = Blueprint('example_blueprint', url_prefix='/example')


@example.route('/')
async def bp_root(request):
    return json({'example': 'blueprint'})


users = {
    'user1': {'username': 'user1', 'password': 'pass1'},
    'user2': {'username': 'user2', 'password': 'pass2'},
}


@example.route('/register', methods=['POST'])
async def register(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise ApiInternalError("Username and password required")

    if username in users:
        raise ApiInternalError('Username already exist')

    users[username] = {'username': username, 'password': password}
    return json({'message': 'Registration successful.'})


@example.route('/login', methods=['POST'])
async def login(request):
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise ApiInternalError('Fail to create book')

    user = users.get(username)

    if not user or user['password'] != password:
        raise ApiInternalError('Fail to create book')

    # Tạo JWT
    token = generate_jwt(username=username)

    return json({'message': 'Login successful.', 'token': token})
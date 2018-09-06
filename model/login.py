from decouple import config
from flask_jwt_extended import create_access_token


def login(username, password):

    if username != config('SYSTEM_USER'):
        return {'message': 'User {} doesn\'t exist'.format(username)}, 401

    if password != config('SYSTEM_PASS'):
        return {'message': 'Wrong credentials'}, 401

    access_token = create_access_token(identity=username)
    return {
        'message': 'Login successful',
        'access_token': access_token
    }, 200

from http import HTTPStatus

from app import app, USERS, models
from flask import request, Response
import json



@app.route('/')
def index():
    return "<h1>Hello world!</h1>"

@app.post('/user/create')
def create_user():
    data = request.get_json()
    id = len(USERS) + 1
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    phone = data['phone']

    if not models.User.is_valid_email(email):
        return Response(
            json.dumps({
                'response': 'email is invalid',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    if not models.User.is_valid_phone(phone):
        return Response(
            json.dumps({
                'response': 'phone is invalid',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    user = models.User(id, first_name, last_name, email, phone)
    USERS.append(user)
    response = Response(
        json.dumps({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'score': user.score,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )
    return response

@app.get('/user/<int:user_id>')
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(
            json.dumps({
                'error': 'Not found',
            }),
            status=HTTPStatus.NOT_FOUND,
            mimetype='application/json',
        )
    user = USERS[user_id]
    response = Response(
        json.dumps({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'score': user.score,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )
    return response
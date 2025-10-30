from http import HTTPStatus
from app import app, USERS, WORKOUTS, models
from flask import request, Response
import json



@app.route('/')
def index():
    return "<h1>Hello world!</h1>"

@app.post('/user/create')
def create_user():
    data = request.get_json()
    user_id = str(len(USERS))
    first_name = data['first_name']
    last_name = data['last_name']
    age = data['age']
    email = data['email']
    phone = data['phone']

    if not models.User.is_valid_email(email) or not models.User.is_valid_phone(phone):
        return Response(
            json.dumps({
                'response': 'email or phone is invalid',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    for user in range(len(USERS)):
        if USERS[user].email == email:
            return Response(
                json.dumps({
                    'error': 'this email already uses',
                }),
                status=HTTPStatus.BAD_REQUEST,
                mimetype='application/json',
            )
    for user in range(len(USERS)):
        if USERS[user].phone == phone:
            return Response(
                json.dumps({
                    'error': 'this phone already uses',
                }),
                status=HTTPStatus.BAD_REQUEST,
                mimetype='application/json',
            )


    user = models.User(user_id, first_name, last_name, age, email, phone)
    USERS.append(user)
    response = Response(
        json.dumps({
            'id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'phone': user.phone,
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
    return Response(
        json.dumps({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )

@app.post('/make-plan')
def user_plan():
    data = request.get_json()
    user_check_id = data['id']
    weight = data['weight']
    workouts = data['workouts']
    goal = data['goal']

    for user in range(len(USERS)):
        if USERS[user].user_id == user_check_id:
            for user_workout in range(len(WORKOUTS)):
                if WORKOUTS[user_workout].user_check_id == user_check_id:
                    return Response(
                        json.dumps({
                            'error': 'user already planned',
                        }),
                    status=HTTPStatus.BAD_REQUEST,
                    mimetype='application/json',
                )
            user_plan = models.Workouts(user_check_id, weight, workouts, goal)
            WORKOUTS.append(user_plan)
            return Response(
                json.dumps({
                    'id': user_plan.user_check_id,
                    'weight': user_plan.weight,
                    'workouts': user_plan.workouts,
                    'goal': user_plan.goal,
                }),
                status=HTTPStatus.OK,
                mimetype='application/json',
            )
    return Response(
        json.dumps({
            'error': 'user does not exist',
        }),
        status=HTTPStatus.NOT_FOUND,
        mimetype='application/json',
    )


@app.get('/check-plan/<int:user_id>')
def get_plan_info(user_id):
    try:
        if WORKOUTS[user_id].user_check_id != str(user_id):
            return Response(
                json.dumps({
                    'error': 'Not found',
                }),
                status=HTTPStatus.NOT_FOUND,
                mimetype='application/json',
            )
    except IndexError:
        return Response(
            json.dumps({
                'error': 'Not found',
            }),
            status=HTTPStatus.NOT_FOUND,
            mimetype='application/json',
        )

    user = WORKOUTS[user_id]
    return Response(
        json.dumps({
            'id': user.user_check_id,
            'weight': user.weight,
            'workouts': user.workouts,
            'goal': user.goal,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )

@app.post('/make-plan/edit')
def doing_workouts():
    data = request.get_json()
    user_check_id = data['id']
    weight_edit = data['weight_edit']
    workouts_edit = data['workouts_edit']

    for user in range(len(WORKOUTS)):
        if WORKOUTS[user].user_check_id == user_check_id:
            WORKOUTS[user].new_weight(weight_edit)
            WORKOUTS[user].quantity_workouts(workouts_edit)
            return Response(
                json.dumps({
                    "id": WORKOUTS[user].user_check_id,
                    "weight": WORKOUTS[user].weight,
                    "workouts": WORKOUTS[user].workouts,
                }),
                status=HTTPStatus.OK,
                mimetype='application/json',
            )
    return Response(
        json.dumps({
            'error': 'user does not exist',
        }),
        status=HTTPStatus.NOT_FOUND,
        mimetype='application/json',
    )


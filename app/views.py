from http import HTTPStatus
from app import app, USERS, STATISTICS, models, WORKOUTS
from flask import request, Response
import json

@app.post('/user/create') #создание пользователя
def create_user():
    data = request.get_json()
    user_id = len(USERS) #id присваивается по порядку с нуля
    first_name = data['first_name']
    last_name = data['last_name']
    age = data['age']
    email = data['email']
    phone = data['phone']

    if not models.User.is_valid_email(email) or not models.User.is_valid_phone(phone): #валидация почты и телефона
        return Response(
            json.dumps({
                'response': 'email or phone is invalid',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    if models.User.is_email_exists(email): #использована ли ранее почта?
        return Response(
            json.dumps({
                'error': 'this email already uses',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    if models.User.is_phone_exists(phone): #использована ли ранее телефон?
        return Response(
            json.dumps({
                'error': 'this phone already uses',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )


    user = models.User(user_id, first_name, last_name, age, email, phone) #пользователь создан
    USERS.append(user)
    return Response(
        json.dumps({
            'RESPONSE': 'USER CREATED',
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

@app.get('/user/<int:user_id>') #получение информации о пользователе
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(
            json.dumps({
                'error': 'User not found',
            }),
            status=HTTPStatus.NOT_FOUND,
            mimetype='application/json',
        )

    user = USERS[user_id]
    return Response(
        json.dumps({
            'RESPONSE': 'USER FOUND',
            'id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )

@app.post('/user/statistics/make-plan') #создание статистики пользователя
def user_plan():
    data = request.get_json()
    user_id = int(data['id'])
    weight = data['weight']
    workouts = data['workouts']
    goal = data['goal']

    if not models.Statistics.is_id_exists(user_id): #проверка id
        return Response(
            json.dumps({
                'error': 'id not found',
            }),
        status=HTTPStatus.BAD_REQUEST,
        mimetype='application/json',
    )
    if models.Statistics.is_statistics_exists(user_id):
        return Response(
            json.dumps({
                'error': 'statistics already exists',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    statistic = models.Statistics(user_id, weight, workouts, goal) #статистика создана
    STATISTICS.append(statistic)
    return Response(
        json.dumps({
            'RESPONSE': 'STATISTICS CREATED',
            'id': statistic.user_id,
            'weight': statistic.weight,
            'workouts': statistic.workouts,
            'goal': statistic.goal,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )

@app.post('/user/statistics/edit') #изменение в статистике
def doing_workouts():
    data = request.get_json()
    user_id = int(data['id'])
    new_weight = str(data['new_weight'])
    workouts_done = str(data['workouts_done'])
    goal = data['goal']

    if not models.Statistics.is_id_exists(user_id): #проверка id
        return Response(
            json.dumps({
                'error': 'id not found',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    if not models.Statistics.is_statistics_exists(user_id):
        return Response(
            json.dumps({
                'error': 'statistics does not exist',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )

    user = STATISTICS[user_id] #изменения приняты
    user.quantity_workouts(workouts_done)
    user.edit_weight(new_weight)
    if goal != 'same':
        user.goal = goal

    return Response(
        json.dumps({
            'RESPONSE': 'STATISTICS UPDATED',
            'id': user.user_id,
            'updated_weight': user.weight,
            'updated_quantity_workouts': user.workouts,
            'goal': user.goal,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )


@app.get('/user/statistics/<int:user_id>') #получение информации из статистики по id
def get_statistics(user_id):
    if not models.Statistics.is_id_exists(user_id): #проверка id
        return Response(
            json.dumps({
                'error': 'id not found',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    if not models.Statistics.is_statistics_exists(user_id):
        return Response(
            json.dumps({
                'error': 'statistics does not exist',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )

    user = STATISTICS[user_id]
    return Response(
        json.dumps({
            'id': user.user_id,
            'weight': user.weight,
            'workouts': user.workouts,
            'goal': user.goal,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )

@app.post('/user/workouts/add') #создание собственной тренировки
def add_workouts():
    data = request.get_json()
    user_id = int(data['id'])
    hands = data['hands']
    abdominal = data['abdominal']
    back = data['back']
    legs = data['legs']
    workout_number = len(WORKOUTS[user_id]) #номер тренировки присваивается по порядку с нуля

    if not models.Statistics.is_statistics_exists(user_id): #проверка id
        return Response(
            json.dumps({
                'error': 'statistic not found',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )

    workout = models.Workout(workout_number, hands, abdominal, back, legs) #тренировка создана
    WORKOUTS[user_id].append(workout)
    return Response(
        json.dumps({
            'RESPONSE': 'WORKOUTS CREATED',
            'id': user_id,
            'workout_number': workout.workout_number,
            'hands': workout.hands,
            'abdominal': workout.abdominal,
            'back': workout.back,
            'legs': workout.legs,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )

@app.post('/user/workouts/edit') #изменение тренировки
def edit_workouts():
    data = request.get_json()
    user_id = int(data['id'])
    workout_number = int(data['workout_number'])
    new_hands = data['new_hands']
    new_abdominal = data['new_legs']
    new_back = data['new_back']
    new_legs = data['new_legs']

    if not models.Statistics.is_statistics_exists(user_id): #проверка id и номера тренировки
        return Response(
            json.dumps({
                'error': 'statistic not found',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    if not models.Workout.is_workout_exists(user_id, workout_number):
        return Response(
            json.dumps({
                'error': 'workout does not exist',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )

    workout = WORKOUTS[user_id][workout_number]
    if new_hands != 'same':
        workout.edit_exersice_hands(new_hands)
    if new_abdominal != 'same':
        workout.edit_exersice_abdominal(new_abdominal)
    if new_back != 'same':
        workout.edit_exersice_back(new_back)
    if new_legs != 'same':
        workout.edit_exersice_legs(new_legs)

    return Response(
        json.dumps({
            'RESPONSE': 'WORKOUTS EDITED',
            'id': user_id,
            'workout_number': workout.workout_number,
            'updated_hands': workout.hands,
            'updated_abdominal': workout.abdominal,
            'updated_back': workout.back,
            'updated_legs': workout.legs,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )


@app.get('/user/workouts/<int:user_id>/<int:workout_number>') #получение информации про свою тренировку по номеру
def get_workouts(user_id, workout_number):
    if not models.Statistics.is_statistics_exists(user_id): #проверка id и номера тренировки
        return Response(
            json.dumps({
                'error': 'statistics not found',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    if not models.Workout.is_workout_exists(user_id, workout_number):
        return Response(
            json.dumps({
                'error': 'workout does not exist',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )

    workout = WORKOUTS[user_id][workout_number]
    return Response(
        json.dumps({
            'RESPONSE': 'WORKOUT',
            'id': user_id,
            'workout_number': workout.workout_number,
            'hands': workout.hands,
            'abdominal': workout.abdominal,
            'back': workout.back,
            'legs': workout.legs,
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )

@app.get('/user/workouts/make-workout/<int:user_id>') #генерация случайной тренировки
def make_workout(user_id):
    if not models.Statistics.is_statistics_exists(user_id):
        return Response(
            json.dumps({
                'error': 'statistics not found',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )
    if len(WORKOUTS[user_id]) == 0:
        return Response(
            json.dumps({
                'error': 'you have no workouts',
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json',
        )

    list_for_workout = models.Workout.make_workout(user_id)  #Элементы в следующем порядке: объект класса Workout;
                                                             # training mode; repetitions; sets
    return Response(
        json.dumps({
            'RESPONSE': 'YOUR WORKOUT, HAVE A NICE TRAINING!',
            'id': user_id,
            'workout_number': list_for_workout[0].workout_number,
            'training_mode': list_for_workout[1],
            'hands': f"{list_for_workout[0].hands}',' {list_for_workout[2]}'x'{list_for_workout[3]}",
            'abdominal': f"{list_for_workout[0].abdominal}',' {list_for_workout[2]}'x'{list_for_workout[3]}",
            'back': f"{list_for_workout[0].back}',' {list_for_workout[2]}'x'{list_for_workout[3]}",
            'legs': f"{list_for_workout[0].legs}',' {list_for_workout[2]}'x'{list_for_workout[3]}",
        }),
        status=HTTPStatus.OK,
        mimetype='application/json',
    )



















from http import HTTPStatus
from app import app, models, WORKOUTS, STATISTICS
from flask import request, Response, url_for
import json


@app.post("/user/workouts/add") #создание собственной тренировки
def workouts_add():
    data = request.get_json()
    user_id = int(data["id"])
    hands = data["hands"]
    abdominal = data["abdominal"]
    back = data["back"]
    legs = data["legs"]
    workout_number = len(WORKOUTS[user_id]) #номер тренировки присваивается по порядку с нуля

    if not models.Statistics.is_statistics_exists(user_id): #проверка id
        return Response(
            f'Statistics does not exist! Firstly, create <a href="{url_for("create_statistics")}">statistics</a>',
            status=HTTPStatus.BAD_REQUEST,
            )

    workout = models.Workout(workout_number, hands, abdominal, back, legs) #тренировка создана
    WORKOUTS[user_id].append(workout)
    statistic = STATISTICS[user_id]
    statistic.add_workout(workout_number)
    return Response(
        json.dumps({
            "RESPONSE": "WORKOUT CREATED",
            "id": user_id,
            "workout_number": workout.workout_number,
        }),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

@app.post("/user/workouts/edit") #изменение тренировки
def workouts_edit():
    data = request.get_json()
    user_id = int(data["id"])
    workout_number = int(data["workout_number"])
    new_hands = data["new_hands"]
    new_abdominal = data["new_abdominal"]
    new_back = data["new_back"]
    new_legs = data["new_legs"]

    if not models.Statistics.is_statistics_exists(user_id): #проверка id и номера тренировки
        return Response(
            f'Statistics does not exist! Firstly, create <a href="{url_for("create_statistics")}">statistics</a>',
            status=HTTPStatus.BAD_REQUEST,
            )
    if not models.Workout.is_workout_exists(user_id, workout_number):
        return Response(
                f'Workout with this number does not exist! Firstly, create <a href="{url_for("workouts_add")}">workouts</a>',
            status=HTTPStatus.BAD_REQUEST,
        )

    workout = WORKOUTS[user_id][workout_number] #внесение изменений
    workout.edit_exersice_hands(new_hands)
    workout.edit_exersice_abdominal(new_abdominal)
    workout.edit_exersice_back(new_back)
    workout.edit_exersice_legs(new_legs)

    return Response(
        json.dumps({
            "RESPONSE": "WORKOUTS EDITED",
            "id": user_id,
            "workout_number": workout.workout_number,
            "updated_hands": workout.hands,
            "updated_abdominal": workout.abdominal,
            "updated_back": workout.back,
            "updated_legs": workout.legs,
        }),
        status=HTTPStatus.ACCEPTED,
        mimetype="application/json",
    )

@app.post("/user/workouts/complete")
def workouts_complete():
    data = request.get_json()
    user_id = int(data["id"])
    workout_number = int(data["workout_number"])
    workouts_done = data["workouts_done"]
    easy_workouts = data["easy_workouts"]
    average_workouts = data["average_workouts"]
    heavy_workouts = data["heavy_workouts"]

    if not models.Statistics.is_statistics_exists(user_id): #проверка id и номера тренировки
        return Response(
            json.dumps({
                "error" : "statistics not found",
        }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )
    if not models.Workout.is_workout_exists(user_id, workout_number):
        return Response(
            json.dumps({
                "error": "workout not found",
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    statistic = STATISTICS[user_id] # изменения приняты
    statistic.quantity_workouts(workouts_done)
    statistic.easy_workouts(easy_workouts)
    statistic.average_workouts(average_workouts)
    statistic.heavy_workouts(heavy_workouts)
    statistic.workout_completed(workout_number)


    return Response(f"Изменения приняты! Ваша статистика тренировок:<br>"
                    f"easy workouts: {statistic.easy_workouts}<br>"
                    f"average workouts: {statistic.average_workouts}<br>"
                    f"heavy workouts: {statistic.heavy_workouts}<br>"
                    f"total workouts: {statistic.workouts}<br>",
                    status=HTTPStatus.ACCEPTED,
    )


@app.get("/user/workouts/<int:user_id>/<int:workout_number>") #получение информации про свою тренировку по номеру
def get_workouts(user_id, workout_number):
    if not models.Statistics.is_statistics_exists(user_id): #проверка id и номера тренировки
        return Response(
            f'Statistics does not exist! Firstly, create <a href="{url_for("create_statistics")}">statistics</a>',
            status=HTTPStatus.BAD_REQUEST,
            )
    if not models.Workout.is_workout_exists(user_id, workout_number):
        return Response(
            f'Workout with this number does not exist! Firstly, create <a href="{url_for("workouts_add")}">workouts</a>',
            status=HTTPStatus.BAD_REQUEST,
        )

    workout = WORKOUTS[user_id][workout_number]
    return Response(
        json.dumps({
            "RESPONSE": "YOUR WORKOUT",
            "id": user_id,
            "workout_number": workout.workout_number,
            "hands": workout.hands,
            "abdominal": workout.abdominal,
            "back": workout.back,
            "legs": workout.legs,
        }),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

@app.get("/user/workouts/make-workout/<int:user_id>") #генерация случайной тренировки
def make_workout(user_id):
    if not models.Statistics.is_statistics_exists(user_id):
        return Response(
            f'Statistics does not exist! Firstly, create <a href="{url_for("create_statistics")}">statistics</a>',
            status=HTTPStatus.BAD_REQUEST,
            )
    if len(WORKOUTS[user_id]) == 0:
        return Response(
            f'Workout with this number does not exist! Firstly, create <a href="{url_for("workouts_add")}">workouts</a>',
            status=HTTPStatus.BAD_REQUEST,
        )

    list_for_workout = models.Workout.make_workout(user_id)  #Элементы в следующем порядке: объект класса Workout;
                                                             # training mode; repetitions; sets
    return Response(
        json.dumps({
            "RESPONSE": "YOUR WORKOUT, HAVE A NICE TRAINING!",
            "id": user_id,
            "workout_number": list_for_workout[0].workout_number,
            "training_mode": list_for_workout[1],
            "hands": f'{list_for_workout[0].hands}"," {list_for_workout[2]}"x"{list_for_workout[3]}',
            "abdominal": f'{list_for_workout[0].abdominal}"," {list_for_workout[2]}"x"{list_for_workout[3]}',
            "back": f'{list_for_workout[0].back}"," {list_for_workout[2]}"x"{list_for_workout[3]}',
            "legs": f'{list_for_workout[0].legs}"," {list_for_workout[2]}"x"{list_for_workout[3]}',
        }),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
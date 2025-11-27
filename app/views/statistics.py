from http import HTTPStatus
from app import app, STATISTICS, models
from flask import request, Response, url_for
import json


@app.post("/user/statistics/create") #создание статистики пользователя
def create_statistics():
    data = request.get_json()
    user_id = int(data["id"])
    weight = data["weight"]
    goal = data["goal"]
    total_workouts = data["total_workouts"]
    easy_workouts = data["easy_workouts"]
    average_workouts = data["average_workouts"]
    heavy_workouts = data["heavy_workouts"]


    if not models.Statistics.is_id_exists(user_id): #проверка id
        return Response(
            json.dumps({
                "error": "id not found",
            }),
        status=HTTPStatus.BAD_REQUEST,
        mimetype="application/json",
    )
    if models.Statistics.is_statistics_exists(user_id):
        return Response(
            json.dumps({
                "error": "statistics already exists",
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )
    statistic = models.Statistics(user_id, weight, goal,  total_workouts,  easy_workouts,  average_workouts,  heavy_workouts) #статистика создана
    STATISTICS.append(statistic)
    return Response(
        json.dumps({
            "RESPONSE": "STATISTICS CREATED",
            "id": statistic.user_id,
        }),
        status=HTTPStatus.CREATED,
        mimetype="application/json",
    )

@app.post("/user/statistics/edit") #изменение в статистике
def statistics_edit():
    data = request.get_json()
    user_id = int(data["id"])
    new_weight = str(data["new_weight"])
    new_goal = data["new_goal"]
    clear_workouts = data["clear_workouts"]

    if not models.Statistics.is_id_exists(user_id): #проверка id
        return Response(
            json.dumps({
                "error": "id not found",
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )
    if not models.Statistics.is_statistics_exists(user_id):
        return Response(f'Statistics does not exist! Firstly, create <a href="{url_for("create_statistics")}">statistics</a>',
            status=HTTPStatus.BAD_REQUEST,
        )

    statistic = STATISTICS[user_id] #изменения приняты
    statistic.edit_weight(new_weight)
    statistic.edit_goal(new_goal)
    statistic.clear_workouts(clear_workouts)

    return Response(
        json.dumps({
            "RESPONSE": "STATISTICS UPDATED",
            "id": statistic.user_id,
            "updated_weight": statistic.weight,
            "updated_goal": statistic.goal,
            "updated_total_workouts": statistic.total_workouts,
            "updated_easy_workouts": statistic.easy_workouts,
            "updated_average_workouts": statistic.average_workouts,
            "updated_heavy_workouts": statistic.heavy_workouts,
        }),
        status=HTTPStatus.ACCEPTED,
        mimetype="application/json",
    )


@app.get("/user/statistics/<int:user_id>") #получение информации из статистики по id
def get_statistics(user_id):
    if not models.Statistics.is_id_exists(user_id): #проверка id
        return Response(
            json.dumps({
                "error": "id not found",
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )
    if not models.Statistics.is_statistics_exists(user_id):
        return Response(
            f'Statistics does not exist! Firstly, create <a href="{url_for("create_statistics")}">statistics</a>',
            status=HTTPStatus.BAD_REQUEST,
            )

    statistic = STATISTICS[user_id]
    most_popular_workout = models.Statistics.workout_leaderboard(statistic.workouts_list)

    return Response(
        json.dumps({
            "id": statistic.user_id,
            "weight": statistic.weight,
            "goal": statistic.goal,
            "total_workouts": statistic.total_workouts,
            "easy_workouts": statistic.easy_workouts,
            "average_workouts": statistic.average_workouts,
            "heavy_workouts": statistic.heavy_workouts,
            "most_popular_workout": most_popular_workout,
        }),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
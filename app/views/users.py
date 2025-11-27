from http import HTTPStatus
from app import app, USERS, models
from flask import request, Response, url_for
import json

@app.post("/user/create") #создание пользователя
def create_user():
    data = request.get_json()
    user_id = len(USERS) #id присваивается по порядку с нуля
    first_name = data["first_name"]
    last_name = data["last_name"]
    age = data["age"]
    email = data["email"]
    phone = data["phone"]

    if not models.User.is_valid_email(email) or not models.User.is_valid_phone(phone): #валидация почты и телефона
        return Response(
            json.dumps({
                "response": "email or phone is invalid",
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )
    if models.User.is_email_exists(email): #использована ли ранее почта?
        return Response(
            json.dumps({
                "error": "this email already uses",
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )
    if models.User.is_phone_exists(phone): #использована ли ранее телефон?
        return Response(
            json.dumps({
                "error": "this phone already uses",
            }),
            status=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )


    user = models.User(user_id, first_name, last_name, age, email, phone) #пользователь создан
    USERS.append(user)
    return Response(
        json.dumps({
            "RESPONSE": "USER CREATED",
            "id": user_id,
        }),
        status=HTTPStatus.CREATED,
        mimetype="application/json",
    )

@app.get("/user/<int:user_id>") #получение информации о пользователе
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(f'User not found! Firstly, create <a href="{url_for("create_user")}">user</a>', status=HTTPStatus.NOT_FOUND)

    user = USERS[user_id]
    return Response(
        json.dumps({
            "RESPONSE": "USER FOUND",
            "id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "phone": user.phone,
        }),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

@app.delete("/user/<int:user_id>")
def delete_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(f'User not found! Firstly, create <a href="{url_for("create_user")}">user</a>', status=HTTPStatus.NOT_FOUND)

    user = USERS[user_id]
    user.status = "deleted"
    return Response(
        json.dumps({
            "RESPONSE": "USER DELETED",
            "id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "phone": user.phone,
        }),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
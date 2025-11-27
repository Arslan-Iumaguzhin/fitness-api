from http import HTTPStatus
import requests
from faker import Faker
import random
from app import __init__, models
from flask import request, Response, url_for
import json

ENDPOINT = "http://127.0.0.1:5000"

def create_statistics_payload():
    fake = Faker()
    user = models.USERS[random.choice(0, len(__init__.USERS))]
    return {
        "id": f"{user.user_id}",
        "weight": f"{random.randint(-1000, 1000)}",
        "goal": f"{fake}",
        "total_workouts": f"{random.randint(-1000, 1000)}",
        "easy_workouts": f"{random.randint(-1000, 1000)}",
        "average_workouts": f"{random.randint(-1000, 1000)}",
        "heavy_workouts": f"{random.randint(-1000, 1000)}",
    }

def test_create_statistics():
    payload = create_statistics_payload()
    create_response = requests.post(f"{ENDPOINT}/user/statistics/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED

    same_payload = create_statistics_payload()
    second_create_response = requests.post(f"{ENDPOINT}/user/statistics/create", json=same_payload)
    assert second_create_response.status_code == HTTPStatus.BAD_REQUEST
    assert second_create_response.json()["error"] == "statistics already exists"


    # todo: Изменение статистики
    user_data = create_response.json()
    user_id = user_data["id"]

    get_response = requests.get(f"{ENDPOINT}/user/{user_id}")
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["age"] == payload["age"]
    assert get_response.json()["email"] == payload["email"]
    assert get_response.json()["phone"] == payload["phone"]
    assert get_response.status_code == HTTPStatus.OK

    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["RESPONSE"] == "USER DELETED"
    assert delete_response.json()["id"] == user_id

def test_create_user_wrong_data():
    payload = create_user_payload()
    payload["phone"] = "123"
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST
    assert create_response.json()["response"] == "email or phone is invalid"

    payload = create_user_payload()
    payload["email"] = "testtest"
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST
    assert create_response.json()["response"] == "email or phone is invalid"
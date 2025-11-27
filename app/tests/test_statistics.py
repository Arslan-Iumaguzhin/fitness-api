from http import HTTPStatus
import requests
from faker import Faker
import random

ENDPOINT = "http://127.0.0.1:5000"
def create_user_payload():
    fake = Faker()
    return {
        "first_name": f"{fake.first_name()}",
        "last_name": f"{fake.last_name()}",
        "age": "21",
        "email": "test@test.ru",
        "phone": "+79999999999",
    }

def test_create_user():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    return create_response.json()["id"]

user_id = test_create_user()

def create_statistics_payload():
    fake = Faker()
    return {
        "id": f"{user_id}",
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

    second_create_response = requests.post(f"{ENDPOINT}/user/statistics/create", json=payload)
    assert second_create_response.status_code == HTTPStatus.BAD_REQUEST
    assert second_create_response.json()["error"] == "statistics already exists"


    get_response = requests.get(f"{ENDPOINT}/user/{user_id}")
    assert get_response.json()["id"] == payload["id"]
    assert get_response.json()["weight"] == payload["weight"]
    assert get_response.json()["goal"] == payload["goal"]
    assert get_response.json()["total_workouts"] == payload["total_workouts"]
    assert get_response.json()["easy_workouts"] == payload["easy_workouts"]
    assert get_response.json()["average_workouts"] == payload["average_workouts"]
    assert get_response.json()["heavy_workouts"] == payload["heavy_workouts"]
    assert get_response.status_code == HTTPStatus.OK

    fake = Faker()
    payload_edit = {
        "id": f"{user_id}",
        "new_weight": f"{random.choice(random.randint(-1000, 1000), "same")}",
        "new_goal": f"{random.choice("same", fake)}",
        "clear_workouts": f"{random.choice("yes", "no")}",
    }

    edit_response = requests.post(f"{ENDPOINT}/user/statistics/edit", json=payload_edit)
    assert edit_response.status_code == HTTPStatus.ACCEPTED
    assert edit_response.json()["RESPONSE"] == "STATISTICS UPDATED"
    assert edit_response.json()["id"] == user_id
    assert edit_response.json()["weight"] in (payload_edit["new_weight"], payload["weight"])
    assert edit_response.json()["goal"] in (payload_edit["new_goal"], payload["goal"])
    assert edit_response.json()["updated_total_workouts"] in (0, payload["total_workouts"])
    assert edit_response.json()["updated_easy_workouts"] in (0, payload["easy_workouts"])
    assert edit_response.json()["updated_average_workouts"] in (0, payload["average_workouts"])
    assert edit_response.json()["updated_heavy_workouts"] in (0, payload["heavy_workouts"])


    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["RESPONSE"] == "USER DELETED"
    assert delete_response.json()["id"] == user_id

    delete_response = requests.delete(f"{ENDPOINT}/user/statistics/delete{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["RESPONSE"] == "STATISTICS DELETED"
    assert delete_response.json()["id"] == user_id


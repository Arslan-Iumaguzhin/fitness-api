from http import HTTPStatus
import requests
from faker import Faker

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

    same_payload = create_user_payload()
    second_create_response = requests.post(f"{ENDPOINT}/user/create", json=same_payload)
    assert second_create_response.status_code == HTTPStatus.BAD_REQUEST
    assert second_create_response.json()["error"] == "this email already uses"

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
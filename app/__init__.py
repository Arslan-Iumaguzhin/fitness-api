from flask import Flask

app = Flask(__name__)

USERS = [] #база данных пользователей
STATISTICS = [] #база данных статистик пользователей
WORKOUTS = [] #база данных тренировок, записанных пользователями (ограничение: максимум 100000 пользователей могут записать тренировки)
for _ in range (100000):
    WORKOUTS.append([])

from app import models
from app import views

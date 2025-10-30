from flask import Flask

app = Flask(__name__)

USERS = []
WORKOUTS = []

from app import views
from app import models
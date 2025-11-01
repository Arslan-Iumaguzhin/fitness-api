from flask import Flask

app = Flask(__name__)

USERS = []
STATISTICS = []

from app import views
from app import models
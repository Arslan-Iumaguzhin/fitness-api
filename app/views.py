from app import app, USERS, STATISTICS, WORKOUTS

@app.route("/")
def index():
    return f"<h1>Hello World!</h1>{USERS}<br>{STATISTICS}<br>{WORKOUTS}"
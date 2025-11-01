import re
from app import USERS, STATISTICS, WORKOUTS
import random

class User:
    def __init__ (self, user_id, first_name, last_name, age, email, phone):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.phone = phone
    @staticmethod
    def is_valid_email(email):
        """Validates an email address using a regular expression."""
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.fullmatch(regex, email):
            return True
        else:
            return False
    @staticmethod
    def is_valid_phone(phone):
        if re.match(r'^\+?[1-9][0-9]{7,14}$',phone):
            return True
        return False

    @staticmethod
    def is_valid_id(check_id):
        if check_id < 0 or check_id >= len(USERS):
            return False
        if USERS[check_id].user_id == check_id:
            return True
        return False

    @staticmethod
    def is_email_exists(check_email):
        for user in USERS:
            if user.email == check_email:
                return True
        return False
    @staticmethod
    def is_phone_exists(check_phone):
        for user in USERS:
            if user.phone == check_phone:
                return True
        return False



class Statistics:
    def __init__ (self, user_id, weight, workouts, goal):
        self.user_id = user_id
        self.weight = weight
        self.workouts = workouts
        self.goal = goal

    def quantity_workouts(self, n):
        self.workouts = str(int(self.workouts) + int(n))
        return None

    def edit_weight(self, new_weight):
        self.weight = new_weight
        return None

    @staticmethod
    def is_id_exists(check_id):
        for user in USERS:
            if user.user_id == check_id:
                return True
        return False

    @staticmethod
    def is_statistics_exists(check_id):
        for statistic in STATISTICS:
            if statistic.user_id == check_id:
                return True
        return False

class Workout:
    def __init__(self, workout_number, hands, abdominal, back, legs):
        self.workout_number = workout_number
        self.hands = hands
        self.abdominal = abdominal
        self.back = back
        self.legs = legs

    def edit_exersice_hands(self, new_hands):
        self.hands = new_hands
        return None

    def edit_exersice_abdominal(self, new_abdominal):
        self.abdominal = new_abdominal
        return None

    def edit_exersice_back(self, new_back):
        self.back = new_back
        return None

    def edit_exersice_legs(self, new_legs):
        self.legs = new_legs
        return None

    @staticmethod
    def is_workout_exists(check_id, workout_number):
        for workout in WORKOUTS[check_id]:
            if workout.workout_number == workout_number:
                return True
        return False

    @staticmethod
    def make_workout(user_id):
        workout = random.choice(WORKOUTS[user_id])
        MODES = ['easy', 'average', 'heavy']
        training_mode = random.choice(MODES)
        if training_mode == 'easy':
            repetitions = random.randint(20,25)
            sets = random.randint(4,5)
        if training_mode == 'average':
            repetitions = random.randint(12, 15)
            sets = random.randint(3, 4)
        if training_mode == ('heavy'):
            repetitions = random.randint(5,7)
            sets = random.randint(2,3)
        return [workout, training_mode, repetitions, sets]









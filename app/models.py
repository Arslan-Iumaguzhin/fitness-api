import re

from phonenumbers.phonenumberutil import country_code_for_region

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
        self.status = "created"
    @staticmethod
    def is_valid_email(email):
        """Validates an email address using a regular expression."""
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(regex, email):
            return True
        else:
            return False
    @staticmethod
    def is_valid_phone(phone):
        if re.match(r"^\+?[1-9][0-9]{7,14}$",phone):
            return True
        return False

    @staticmethod
    def is_valid_id(check_id):
        return check_id >= 0 and check_id < len(USERS) and USERS[check_id].status == "created"

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
    def __init__ (self, user_id, weight, goal, total_workouts, easy_workouts, average_workouts, heavy_workouts, workouts_list=[]):
        self.user_id = user_id
        self.weight = weight
        self.goal = goal
        self.total_workouts = total_workouts
        self.easy_workouts = easy_workouts
        self.average_workouts = average_workouts
        self.heavy_workouts = heavy_workouts
        self.workouts_list = workouts_list
        self.status = "created"

    def quantity_workouts(self, new_workouts):
        self.total_workouts = str(int(self.total_workouts) + int(new_workouts))
        return None

    def quantity_workouts_easy(self, new_easy_workouts):
        self.easy_workouts = str(int(self.easy_workouts) + int(new_easy_workouts))
        return None

    def quantity_workouts_average(self, new_average_workouts):
        self.average_workouts = str(int(self.average_workouts) + int(new_average_workouts))
        return None

    def quantity_workouts_heavy(self, new_heavy_workouts):
        self.heavy_workouts = str(int(self.heavy_workouts) + int(new_heavy_workouts))
        return None

    def edit_weight(self, new_weight):
        if new_weight != "same":
            self.weight = new_weight
        return None

    def edit_goal(self, new_goal):
        if new_goal != "same":
            self.goal = new_goal
        return None

    def clear_statistics(self, answer):
        edited_answer = answer.lower()
        if edited_answer == "да" or edited_answer == "yes":
            self.total_workouts = 0
            self.easy_workouts = 0
            self.average_workouts = 0
            self.heavy_workouts = 0
        return None

    def add_workout(self, new_workout):
        self.workouts_list.append({new_workout: 0})
        return None

    def workout_completed(self, workout_done):
        self.workouts_list[workout_done][workout_done] += 1
        return None

    @staticmethod
    def workout_leaderboard(LIST):
        if len(LIST) == 0:
            return f"there are no workouts"
        counter = 0
        name = "empty"
        for workout in range(len(LIST)):
            if LIST[workout][workout] > counter:
                counter = LIST[workout][workout]
                name = workout
        if name is str:
            return f"you have no completed workouts"
        if name is int:
            return f"most popular workout {name}"


    @staticmethod
    def is_id_exists(check_id):
        for user in USERS:
            if user.user_id == check_id and user.status == "created":
                return True
        return False

    @staticmethod
    def is_statistics_exists(check_id):
        for statistic in STATISTICS:
            if statistic.user_id == check_id and statistic.status == "created":
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
        if new_hands != "same":
            self.hands = new_hands
        return None

    def edit_exersice_abdominal(self, new_abdominal):
        if new_abdominal != "same":
            self.abdominal = new_abdominal
        return None

    def edit_exersice_back(self, new_back):
        if new_back != "same":
            self.back = new_back
        return None

    def edit_exersice_legs(self, new_legs):
        if new_legs != "same":
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
        MODES = ["easy", "average", "heavy"]
        training_mode = random.choice(MODES)
        if training_mode == "easy":
            repetitions = random.randint(20,25)
            sets = random.randint(4,5)
        if training_mode == "average":
            repetitions = random.randint(12, 15)
            sets = random.randint(3, 4)
        if training_mode == ("heavy"):
            repetitions = random.randint(5,7)
            sets = random.randint(2,3)
        return [workout, training_mode, repetitions, sets]









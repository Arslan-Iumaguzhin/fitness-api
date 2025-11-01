import re
from app import USERS, STATISTICS

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
        for user in STATISTICS:
            if user.user_id == check_id:
                return True
        return False





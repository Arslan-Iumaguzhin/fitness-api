import re

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


class Workouts:
    def __init__ (self, user_check_id, weight, workouts, goal):
        self.user_check_id = user_check_id
        self.weight = weight
        self.workouts = workouts
        self.goal = goal
    def quantity_workouts(self, n):
        self.workouts = int(self.workouts) + int(n)
        return None
    def new_weight(self, new_weight):
        self.weight = new_weight
        return None



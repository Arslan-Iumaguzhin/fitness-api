Ты — бэкенд-разработчик API для платформы, помогающей пользователям отслеживать физическую активность.
Необходимо создать полноценный сервис на Flask, который выполняет следующие функции:

Основные функции:

Создание пользователя
Создает пользователя, проверяет корректность e-mail и номера телефона, а также проверяет: зарегестрирован ли пользователь ранее?
Хранит имя, возраст и цель пользователя (например, «похудеть», «набрать массу», «поддерживать форму»).

Статистика
Выдает данные по конкретному пользователю
(например, статистику тренировок, количество выполненных упражнений и т. д.).

Создание и генерация тренировки
Доступно добавление персональной тренировки, а также рандомный выбор тренировки, ее типа и кол-ва подходов и повторений
Пользователь выполняет тренировку и записывает тренировку как выполненную


Допущения:

Все объекты (пользователи, статистика, тренировки) можно хранить в runtime (например, в списках или словарях).

Проверку существования e-mail и номера телефона можно реализовать через регулярные выражения, без подключения внешних библиотек.


Необходимо:

Код должен быть отформатирован (например, при помощи black).

Проект должен содержать четкую структуру (например, app.py, routes/, models/, utils/).

Все основные функции должны быть доступны через REST API (GET, POST, PUT, DELETE, если нужно).

Примерный стек:

Python 3.10+

Flask

Regex (для валидации)

Random (для генерации тренировок и вопросов)

#Запросы и ответы

- Создание пользователя "POST /user/create"

Reqeust example:
'''json
{
    "first_name": "name",
    "last_name": "last_name",
    "age": "age",
    "email": "real_email",
    "phone": "real_phone",
}
'''

Response example
'''json
{
    "RESPONSE": "USER CREATED"
    "id" : "id",
}
'''

- Поиск пользователя "GET /user/id"

Response example:
'''json
{
    "RESPONSE": "USER FOUND",
    "id": "id",
    "first_name": "name",
    "last_name": "last_name",
    "email": "email",
    "phone": "phone",
}
'''

- Добавление собственной статистики "POST /user/statistics/create"

Request example:
'''json
{
    "id" : "id",
    "weight" : "number",
    "goal" : "string",
    "total_workouts" : "number",
    "easy_workouts" : "number",
    "average_workouts" : "number",
    "heavy_workouts" : "number",
}
'''

Response example:
'''json
{
    "RESPONSE": "STATISTICS CREATED",
    "id": "id",
}
'''

- Изменение статистики "POST /user/statistics/edit"

Request example:
'''json
{
    "id": "id",
    "new_weight: "number/same",
    "new_goal": "string/same",
    "clear_workouts": "yes/no",
}
'''

Response example:
'''json
{
    "RESPONSE": "STATISTICS UPDATED",
    "id": "id",
    "updated_weight": "number",
    "updated_goal": "string",
    "updated_total_workouts": "number",
    "updated_easy_workouts": "number",
    "updated_average_workouts": "number",
    "updated_heavy_workouts": "number",
}
'''

- Посмотреть статистику "GET /user/statistics/id"

Response example:
'''json
{
    "id": "id",
    "weight": "number",
    "goal": "string",
    "total_workouts": "number",
    "easy_workouts": "number",
    "average_workouts": "number",
    "heavy_workouts": "number",
    "most_popular_workout": "number",
}
'''

- Добавить новую тренировку "GET /user/workouts/add"

Request example:
'''json
{
    "id": "id",
    "hands": "string",
    "abdominal": "string",
    "back": "string",
    "legs": "string",
}
'''

Response example:
'''json
{
    "RESPONSE": "WORKOUT CREATED",
    "id": "id",
    "workout_number": "workout_number",
}
'''

- Изменение тренировки "POST /user/workouts/edit"

Request example:
'''json
{
    "id": "id",
    "workout_number": "workout_number",
    "new_hands": "string/same",
    "new_abdominal": "string/same",
    "new_back": "string/same",
    "new_leg": "string/same",
}
'''

Response example:
'''json
{
    "RESPONSE": "WORKOUTS EDITED",
    "id": "id",
    "workout_number": "workout_number",
    "updated_hands": "string",
    "updated_abdominal": "string",
    "updated_back": "string",
    "updated_legs": "string",
}
'''

- Запись выполненной тренировки "POST /user/workouts/complete"

Request example:
'''json
{
    "id": "id",
    "workout_number": "workout_number",
    "workouts_done": "number",
    "easy_workouts": "number",
    "average_workouts": "number",
    "heavy_workouts": "number",
}
'''

Response example:
    "Изменения приняты! Ваша статистика тренировок:"
    "easy workouts: "number"
    "average workouts: "number"
    "heavy workouts: "number
    "total workouts: "number

- Просмотр тренировки "GET /user/workouts/id/workout_number"

Response example:
'''json
{
    "RESPONSE": "YOUR WORKOUT",
    "id": "id",
    "workout_number": "workout_number",
    "hands": "string",
    "abdominal": "string",
    "back": "string",
    "legs": "string",
}
'''

- Генерация тренировки "GET /user/workouts/make-workout/id"

Response example:
'''json
    "RESPONSE": "YOUR WORKOUT, HAVE A NICE TRAINING!",
    "id": "id",
    "workout_number": "workout_number",
    "training_mode": "training_mode",
    "hands": "exercise, sets, repetitions",
    "abdominal": "exercise, sets, repetitions",
    "back": "exercise, sets, repetitions",
    "legs": "exercise, sets, repetitions",
}
'''
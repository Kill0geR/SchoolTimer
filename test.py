import time
import UntisAPI
import requests

teachers = UntisAPI.get_all_teachers()


def get_gender(name):
    dict_gender = {"female": "der Frau Professor", "male": "dem Herrn Professor"}
    url = f"https://api.genderize.io/?name={name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['gender'] is not None:
            return dict_gender[data['gender']]


with open("all_teacher_genders.txt", "r+") as f:
    all_teacher_genders = [each.split()[2] for each in f.readlines()]
    print(all_teacher_genders)

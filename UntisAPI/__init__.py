import webuntis
from datetime import datetime
import ast


def login(username, password):
    try:
        s = webuntis.Session(
            server='neilo.webuntis.com',
            username=username,
            password=password,
            school='borg-graz-monsbergergasse',
            useragent='WebUntis Test'
        )
        s.login()
        return s
    except NameError:
        raise Exception('Du musst Webuntis herunterladen du Hund\nAlso `pip install webuntis`')


def get_9t_lessons(username, password):
    s = login(username, password)
    klassen = s.klassen()
    all_lessons = {}
    latin_french = {}
    today_lessons = []
    in_our_class = {}
    substitute_lessons = []
    long_names = {'GWB': 'Geographie', 'PUP': 'Philosophie', 'INW': 'Internet Working', 'BIU': 'Biologie', 'BSPK': 'Turnen', 'R': 'Religion'}
    for klasse in klassen:
        cid = klasse.id
        clas = klassen.filter(id=cid)[0]
        now = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        tt = s.timetable_extended(klasse=clas, start=now, end=now)

        for stunde in tt:
            try:
                if clas.name == "9t" and stunde.code != "cancelled" and stunde.subjects[0].name not in ["FRD", "UBS"]:
                    if stunde.original_teachers:
                        substitute_lessons.append(stunde.end.strftime("%H:%M"))

                    short_name = stunde.subjects[0].name
                    if stunde.end.strftime("%H:%M") not in all_lessons:
                        all_lessons[stunde.end.strftime("%H:%M")] = [stunde.teachers[0].name, stunde.rooms[0].name, stunde.subjects[0].long_name.title() if short_name not in long_names else long_names[short_name]]
                    else: latin_french[stunde.end.strftime("%H:%M")] = [stunde.teachers[0].name, stunde.rooms[0].name, stunde.subjects[0].long_name.title() if short_name not in long_names else long_names[short_name]]

                    today_lessons.append(stunde.start.strftime("%H:%M"))
                    today_lessons.append(stunde.end.strftime("%H:%M"))

                if stunde.rooms[0].name == "U35" and clas.name not in ["9t", "9s"]:
                    if stunde.end.strftime("%H:%M") not in in_our_class:
                        in_our_class[stunde.end.strftime("%H:%M")] = ["-".join(clas.name)]

                    else: in_our_class[stunde.end.strftime("%H:%M")].append("-".join(clas.name))

            except Exception as e:
                pass

    try:
        sorted_lessons = sorted(list(set(today_lessons)))
        sorted_lessons[0] = "07:50"

    except IndexError as Ie:
        print(Ie)
        pass
    return dict(sorted(all_lessons.items())), latin_french, sorted_lessons, in_our_class, substitute_lessons


def get_all_teachers():
    with open("all_teacher_genders.txt", "r", encoding="utf-8") as f:
        teachers_gender = f.readlines()

    all_teachers = {teacher.split("*")[0].strip(): [teacher.split("*")[1].strip(), teacher.split("*")[2].strip()] for teacher in teachers_gender}
    return all_teachers

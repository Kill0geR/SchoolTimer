import webuntis
from datetime import datetime


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


def get_teacher_table(username, password):
    s = login(username, password)
    klassen = s.klassen()
    for klasse in klassen:
        cid = klasse.id
        clas = klassen.filter(id=cid)[0]
        now = datetime.now()
        tt = s.timetable_extended(klasse=clas, start=now, end=now)

        for stunde in tt:
            if str(clas.name) == "9t":
                return stunde.subjects[0]

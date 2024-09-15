import datetime
from pygame import mixer, time
from UntisAPI import get_9t_lessons, get_all_teachers
from gtts import gTTS
from io import BytesIO
import time as tm


def talk(text):
    print(text)
    tts = gTTS(text=text, lang='de')
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)

    mixer.init()

    tm.sleep(0.5)
    audio_fp.seek(0)
    mixer.music.load(audio_fp, "mp3")
    mixer.music.play()

    while mixer.music.get_busy():
        continue


def play_bell():
    mixer.init()

    mixer.music.load("bell/school_bell_2.mp3")

    mixer.music.play()

    while mixer.music.get_busy():
        time.Clock().tick(10)

end_time = ['08:40', '09:35', '10:30', '11:35', '12:25', '13:15', '14:10', '15:00', '15:50', '16:40', '17:30', '18:20']

username, password = "Bashirufaw", "7nfScyThnzbd$"
lessons, latin_french, all_lessons_hours = get_9t_lessons(username, password)
all_teachers = get_all_teachers(username, password)

week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"]
today = datetime.datetime.now().strftime("%A")

while True:
    now = datetime.datetime.now()
    now_time = now.strftime("%H:%M")
    day_name = now.strftime("%A")

    if day_name != today:
        today = day_name
        lessons, latin_french, all_lessons_hours = get_9t_lessons(username, password)

    if day_name in week_days and now_time in all_lessons_hours:
        print(now_time)
        play_bell()

        if now_time == all_lessons_hours[0]:
            start_next_time = all_lessons_hours[all_lessons_hours.index(now_time) + 1]
            talk(f"Die erste Stunde beginnt jetzt. Ihr habt {lessons[start_next_time][2]} "
                 f"mit {all_teachers[lessons[start_next_time][0]][-1]} {all_teachers[lessons[start_next_time][0]][0]} im Raum {lessons[start_next_time][1]}, Viel Spaß")

        if now_time in end_time:
            if now_time == all_lessons_hours[-1]:
                if day_name != "Friday": talk("Schulende. Ich wünsche euch noch einen schönen Tag")
                else: talk("Schulende. Ich wünsche euch noch ein schönes Wochenende")

            else:
                get_next_time = end_time[end_time.index(now_time) + 1]
                gender_teacher = all_teachers[lessons[get_next_time][0]][-1]
                teacher_name = all_teachers[lessons[get_next_time][0]][0]
                if get_next_time in latin_french:
                    first_lesson, second_lesson = lessons[get_next_time][2], latin_french[get_next_time][2]
                    talk(f"Die nächsten Stunden sind {first_lesson} und {second_lesson}. "
                         f"{first_lesson} ist mit {gender_teacher} {teacher_name} im Raum {lessons[get_next_time][1]}. "
                         f"{second_lesson} ist mit {all_teachers[latin_french[get_next_time][0]][-1]} {all_teachers[latin_french[get_next_time][0]][0]} im Raum {latin_french[get_next_time][1]}, Viel Spaß")
                else:
                    talk(f"Die nächste Stunde ist {lessons[get_next_time][2]} mit {gender_teacher} {teacher_name} im Raum {lessons[get_next_time][1]}, Viel Spaß")
                # Das ist dann für die Ansage Lee

        all_lessons_hours.remove(now_time)

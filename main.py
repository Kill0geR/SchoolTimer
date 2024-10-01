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


def play_bell(current_time):
    mixer.init()

    bell = "bell/school_bell_2.mp3"
    if current_time in lessons:
        if lessons[current_time][-1] == "Religion":
            bell = "bell/church_bell.mp3"
    mixer.music.load(bell)

    mixer.music.play()

    while mixer.music.get_busy():
        time.Clock().tick(10)


end_time = ['08:40', '09:35', '10:30', '11:35', '12:25', '13:15', '14:10', '15:00', '15:50', '16:40', '17:30', '18:20']

username, password = "Bashirufaw", "7nfScyThnzbd$"
all_teachers = get_all_teachers()

week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
today = ""

while True:
    now = datetime.datetime.now()
    now_time = now.strftime("%H:%M")
    day_name = now.strftime("%A")

    if day_name != today and day_name in week_days:
        today = day_name
        lessons, latin_french, all_lessons_hours, in_our_class = get_9t_lessons(username, password)
        print(lessons)

    if day_name in week_days and now_time in all_lessons_hours:
        play_bell(now_time)

        if now_time == "07:50":
            start_next_time = all_lessons_hours[all_lessons_hours.index(now_time) + 1]
            talk(f"Die erste Stunde beginnt jetzt. Ihr habt {lessons[start_next_time][2]} "
                 f"mit {all_teachers[lessons[start_next_time][0]][-1]} {all_teachers[lessons[start_next_time][0]][0]} im Raum {lessons[start_next_time][1]}, Viel Spaß")

        if now_time in end_time:
            if now_time == all_lessons_hours[-1]:
                if day_name != "Friday": talk("Schulende. Ich wünsche euch noch einen schönen Tag")
                else: talk("Schulende. Ich wünsche euch noch ein schönes Wochenende")

            else:
                get_before_time = end_time[end_time.index(now_time)]
                get_next_time = end_time[end_time.index(now_time) + 1]

                if get_next_time in in_our_class:
                    info_text = f"Übrigens ist in der nächsten Stunde die {' und '.join(in_our_class[get_next_time]) if len(in_our_class[get_next_time]) == 2 else in_our_class[get_next_time][0]} in eurer Klasse."
                else: info_text = ""

                if lessons[get_next_time][-1] != lessons[get_before_time][-1]:
                    if lessons[get_before_time][-1] == "Latein" and latin_french:
                        before_teacher_gender_lat = " ".join(all_teachers[latin_french[get_before_time][0]][-1].split()[1:]).replace("Herrn", "Herr").strip()
                        before_teacher_name_lat = all_teachers[latin_french[get_before_time][0]][0]
                        talk(f"Auf wiedersehen {before_teacher_gender_lat} {before_teacher_name_lat}")

                    else:
                        before_teacher_gender = " ".join(all_teachers[lessons[get_before_time][0]][-1].split()[1:]).replace("Herrn", "Herr").strip()
                        before_teacher_name = all_teachers[lessons[get_before_time][0]][0]
                        talk(f"Auf wiedersehen {before_teacher_gender} {before_teacher_name}")

                    gender_teacher = all_teachers[lessons[get_next_time][0]][-1]
                    teacher_name = all_teachers[lessons[get_next_time][0]][0]
                    if get_next_time in latin_french:
                        first_lesson, second_lesson = lessons[get_next_time][2], latin_french[get_next_time][2]
                        talk(f"Die nächsten Stunden sind {first_lesson} und {second_lesson}. "
                             f"{first_lesson} ist mit {gender_teacher} {teacher_name} im Raum {lessons[get_next_time][1]}. "
                             f"{second_lesson} ist mit {all_teachers[latin_french[get_next_time][0]][-1]} {all_teachers[latin_french[get_next_time][0]][0]} im Raum {latin_french[get_next_time][1]}, Viel Spaß. {info_text}")
                    else:
                        eth = False
                        if lessons[get_next_time][-1] == "Ethik":
                            talk(f"Schulende. Ich wünsche euch noch einen schönen Tag außer Ali Zakeri der hat nämlich {lessons[get_next_time][2]} mit {gender_teacher} {teacher_name} im Raum {lessons[get_next_time][1]}, Viel Spaß Ali Zakeri Hahahaha")
                            eth = True

                        if not eth:
                            talk(f"Die nächste Stunde ist {lessons[get_next_time][2]} mit {gender_teacher} {teacher_name} im Raum {lessons[get_next_time][1]}, Viel Spaß. {info_text}")
                    # Das ist dann für die Ansage Lee

        all_lessons_hours.remove(now_time)

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


def bye_prof():
    try:
        if get_before_time not in in_our_class:
            if lessons[get_before_time][-1] == "Latein" and latin_french:
                before_teacher_gender_lat = " ".join(
                    all_teachers[latin_french[get_before_time][0]][-1].split()[1:]).replace("Herrn", "Herr").strip()
                before_teacher_name_lat = all_teachers[latin_french[get_before_time][0]][0]
                talk(f"Auf wiedersehen {before_teacher_gender_lat} {before_teacher_name_lat}")

            else:
                before_teacher_gender = " ".join(all_teachers[lessons[get_before_time][0]][-1].split()[1:]).replace("Herrn",
                                                                                                                    "Herr").strip()
                before_teacher_name = all_teachers[lessons[get_before_time][0]][0]
                talk(f"Auf wiedersehen {before_teacher_gender} {before_teacher_name}")

        else:
            before_teacher_gender_lat = " ".join(
                all_teachers[in_our_class[get_before_time][-1]][-1].split()[1:]).replace("Herrn",
                                                                                         "Herr").strip()
            before_teacher_name_lat = all_teachers[in_our_class[get_before_time][-1]][0]
            talk(f"Auf wiedersehen {before_teacher_gender_lat} {before_teacher_name_lat}")
    except KeyError:
        pass


def play_bell(current_time):
    print("\nbell is playing\n")
    mixer.init()
    mixer.pre_init(44100, -16, 2, 4096)

    bell = "bell/school_bell_2.mp3"
    if current_time in lessons:
        if lessons[current_time][-1] == "Religion":
            bell = "bell/church_bell.mp3"
    mixer.music.load(bell)

    mixer.music.play()

    while mixer.music.get_busy():
        time.Clock().tick(10)


def next_lesson():
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
            talk(
                f"Schulende. Ich wünsche euch noch einen schönen Tag außer Ali Zakeri der hat nämlich {lessons[get_next_time][2]} mit {gender_teacher} {teacher_name} im Raum {lessons[get_next_time][1]}, Viel Spaß Ali Zakeri Hahahaha")
            eth = True

        if not eth:
            if get_next_time in substitution:
                sub_text = " wird suppliert und"
            else:
                sub_text = ""
            talk(
                f"Die nächste Stunde{sub_text} ist {lessons[get_next_time][2]} mit {gender_teacher} {teacher_name} im Raum {lessons[get_next_time][1]}, Viel Spaß. {info_text}")


end_time = ['08:40', '09:35', '10:30', '11:35', '12:25', '13:15', '14:10', '15:00', '15:50', '16:40', '17:30', '18:20']
all_times = list(set(['07:50', '08:40', '08:45', '09:35', '09:40', '10:30', '10:45', '11:35', '11:35', '12:25', '12:25', '13:15', '13:20', '14:10', '14:10', '15:00']))

username, password = "Bashirufaw", "7nfScyThnzbd$"
all_teachers = get_all_teachers()

week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
today = ""

while True:
    now = datetime.datetime.now()
    now_time = "07:50"
    day_name = now.strftime("%A")

    if day_name != today and day_name in week_days:
        today = day_name
        lessons, latin_french, all_lessons_hours, in_our_class, substitution = get_9t_lessons(username, password)
        print(lessons)
        print(in_our_class)

    if day_name in week_days and (now_time in all_lessons_hours or now_time in all_times):
        play_bell(now_time)



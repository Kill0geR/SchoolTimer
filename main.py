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

end_time = ['08:40', '09:35', '10:30', '11:35', '12:25', '13:15', '14:10', '15:00', '15:50', '16:40', '17:30', '18:20']
all_time = list(set(end_time + ['07:50', '08:45', '09:40', '10:45', '11:35', '12:25', '13:20', '14:10', '14:50', '15:00', '15:50', '16:40', '17:30']))
all_time_copy = all_time.copy()

username, password = "Bashirufaw", "7nfScyThnzbd$"
lessons, latin_french = get_9t_lessons(username, password)
all_teachers = get_all_teachers(username, password)

while True:
    now = datetime.datetime.now()
    now_time = now.strftime("%H:%M")

    if now_time in all_time_copy:
        print(now_time)
        mixer.init()

        mixer.music.load("bell/school_bell_2.mp3")

        mixer.music.play()

        while mixer.music.get_busy():
            time.Clock().tick(10)

        if now_time in end_time:
            get_next_time = end_time[end_time.index(now_time) + 1]
            gender_teacher = all_teachers[lessons[get_next_time][0]][-1]
            teacher_name = all_teachers[lessons[get_next_time][0]][0]
            if get_next_time in latin_french:
                first_lesson, second_lesson = lessons[get_next_time][2], latin_french[get_next_time][2]
                talk(f"Die nächste Stunden sind {first_lesson} und {second_lesson}. "
                     f"{first_lesson} ist mit {gender_teacher} {teacher_name} im Raum {lessons[get_next_time][1]}. "
                     f"{second_lesson} ist mit {all_teachers[latin_french[get_next_time][0]][-1]} {all_teachers[latin_french[get_next_time][0]][0]} im Raum {latin_french[get_next_time][1]}, Viel Spaß")
            else:
                talk(f"Die nächste Stunde ist {lessons[get_next_time][2]} mit {gender_teacher} {teacher_name} im Raum {lessons[get_next_time][1]}, Viel Spaß")
            # Das ist dann für die Ansage Lee

        all_time_copy.remove(now_time)

    if not all_time_copy:
        all_time_copy = all_time.copy()

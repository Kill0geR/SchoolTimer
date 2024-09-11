import datetime
import pyttsx3
from pygame import mixer, time


def talk(text):
    engine.say(text)
    engine.runAndWait()

end_time = ['08:40', '09:35', '10:30', '11:35', '12:25', '13:15', '14:10', '15:00', '15:50', '16:40', '17:30', '18:20', "15:10"]
all_time = list(set(end_time + ['07:50', '08:45', '09:40', '10:45', '11:35', '12:25', '13:20', '14:10', '14:50', '15:00', '15:50', '16:40', '17:30', "15:10"]))
all_time_copy = all_time.copy()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)
engine.setProperty("voice", "de")

while True:
    now = datetime.datetime.now()
    now_time = now.strftime("%H:%M")

    if now_time in all_time_copy:
        mixer.init()

        mixer.music.load("bell/school_bell.mp3")

        mixer.music.play()

        while mixer.music.get_busy():
            time.Clock().tick(10)

        if now_time in end_time:
            pass
            # Das ist dann für die Ansage Lee

        all_time_copy.remove(now_time)

    if not all_time_copy:
        all_time_copy = all_time.copy()

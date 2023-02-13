import speech_recognition as s_r
import pyaudio as pa
import pyttsx3


class BotTalk:
    def __init__(self):
        self.text_to_speach = pyttsx3.init()

    def say_speach(self, text):
        self.text_to_speach.setProperty('rate', 150)  # setting up new voice rate
        self.text_to_speach.say(text)
        self.text_to_speach.runAndWait()

    def input_speach(self):
        r = s_r.Recognizer()
        with s_r.Microphone(device_index=1) as source:
            print("Say now!!!!")
            # r.adjust_for_ambient_noise(source)  # reduce noise
            audio = r.listen(source,phrase_time_limit=4)  # take voice input from the microphone
            said = ""
            try:
                said = r.recognize_google(audio,language='en-in')
            except Exception as e:
                print("Exception: " + str(e))

        return said  # to return voice into text

import speech_recognition as sr

class WakeListener:
    
    def __init__(self, wake_words):
        self.wake_words = wake_words

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Waiting for wake word...")

            while True:
                try:
                    audio = r.listen(source)
                    command = r.recognize_google(audio).lower()
                    print("Wake Check:", command)

                    for word in self.wake_words:
                        if word in command:
                            return True

                except:
                    continue

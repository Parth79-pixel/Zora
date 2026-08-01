import datetime

class Greet:
    
    def wish(self, speech):
        hour = int(datetime.datetime.now().hour)

        if hour < 12:
            speech.speak("Good morning")
        elif hour < 16:
            speech.speak("Good afternoon")
        else:
            speech.speak("Good evening")

        speech.speak("I am Zora. How can I help you?")

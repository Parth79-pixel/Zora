import os
import sys
import cv2
import random
import threading
import webbrowser
import wikipedia
import pyautogui
import pygetwindow as gw
from requests import get
import pywhatkit as kit
import datetime
import time
from ai import ZoraAI


class ZoraCommands:

    def __init__(self):
        self.camera_open = False
        self.cap = None
        self.ai = ZoraAI()

    # ================= MAIN HANDLER ================= #

    def handle(self, query, speech):
        if query == "none" or query.strip() == "":
            return
        query = query.lower()
        query = query.replace("pen ", "open ")
        query = query.replace("cam ", "camera ")

        if "open notepad" in query or "opennotepad" in query:
            os.startfile("C:\\Windows\\System32\\notepad.exe")

        elif "close notepad" in query:
            speech.speak("Okay sir, closing notepad")
            os.system("taskkill /f /im notepad.exe >nul 2>&1")

        elif "open adobe reader" in query:
            os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe Reader XI.lnk")

        elif "close adobe reader" in query:
            speech.speak("Okay sir, closing adobe reader")
            os.system("taskkill /f /im AcroRd32.exe >nul 2>&1")

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "close command prompt" in query:
            speech.speak("Okay sir, closing command prompt")
            os.system("taskkill /f /im cmd.exe >nul 2>&1")

        elif "open webcam" in query:
            self.open_webcam()

        elif "close webcam" in query and self.camera_open:
            speech.speak("Okay sir, closing webcam")
            self.camera_open = False

        elif "play music" in query:
            music_dir = "C:\\Users\\hp\\Music"
            song = random.choice(os.listdir(music_dir))
            os.startfile(os.path.join(music_dir, song))

        elif "close music" in query:
            speech.speak("Okay sir, closing music")
            os.system("taskkill /f /im wmplayer.exe >nul 2>&1")

        elif "ip address" in query:
            ip = get("https://api.ipify.org").text
            speech.speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            self.search_wikipedia(query, speech)

        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")

        elif "close youtube" in query:
            self.close_window("Youtube", speech)

        elif "open facebook" in query:
            webbrowser.open("https://www.facebook.com")

        elif "close facebook" in query:
            self.close_window("Facebook", speech)

        elif "open whatsapp" in query:
            os.system("start whatsapp:")

        elif "close whatsapp" in query:
            speech.speak("Okay sir, closing whatsapp")
            os.system("taskkill /f /im Whatsapp.exe >nul 2>&1")

        elif "open instagram" in query:
            os.startfile("C:\\Users\\hp\\OneDrive\\Desktop\\Instagram.lnk")

        elif "close instagram" in query:
            self.close_window("Instagram", speech)

        elif "open google chrome" in query:
            speech.speak("What should I search?")
            search = speech.takecommand()
            webbrowser.open(f"https://www.google.com/search?q={search}")

        elif "close google chrome" in query:
            speech.speak("Okay sir, closing chrome")
            os.system("taskkill /f /im chrome.exe >nul 2>&1")

        elif "play video on youtube" in query:
            speech.speak("What should I play?")
            song = speech.takecommand()
            kit.playonyt(song)

        elif "set alarm" in query:
            self.set_alarm(speech)

        elif "clear memory" in query:
            self.ai.history.clear()
            speech.speak("Memory Cleared")
        
        elif any(x in query for x in ["stop", "exit", "quit", "thanks"]):
            speech.speak("Thanks for using me sir")
            sys.exit()
        
        else:
            answer = self.ai.ask(query)
            speech.speak(answer)

    # ================= HELPERS ================= #

    def open_webcam(self):
        if not self.camera_open:
            self.camera_open = True

            def webcam_thread():
                self.cap = cv2.VideoCapture(0)
                while self.camera_open:
                    ret, img = self.cap.read()
                    if not ret:
                        break
                    cv2.imshow("Webcam", img)
                    if cv2.waitKey(1) == 27:
                        break

                self.cap.release()
                cv2.destroyAllWindows()
                self.camera_open = False

            threading.Thread(target=webcam_thread).start()

    def search_wikipedia(self, query, speech):
        speech.speak("Searching Wikipedia")
        for word in ["wikipedia", "who is", "what is", "tell me about"]:
            query = query.replace(word, "")
        try:
            result = wikipedia.summary(query.strip(), sentences=5)
            speech.speak(result)
        except:
            speech.speak("Sorry, I could not find anything")

    def close_window(self, title, speech):
        try:
            for window in gw.getWindowsWithTitle(title):
                if window.visible:
                    window.activate()
                    pyautogui.hotkey("alt", "f4")
                    return
            speech.speak(f"No {title} window found")
        except:
            speech.speak("Something went wrong")

    def set_alarm(self, speech):
        speech.speak("Tell hours")
        hour = int(speech.takecommand())

        speech.speak("Tell minutes")
        minute = int(speech.takecommand())

        speech.speak(f"Alarm set for {hour}:{minute}")

        while True:
            now = datetime.datetime.now()
            if now.hour == hour and now.minute == minute:
                speech.speak("Wake up sir, alarm is ringing")
                music_dir = "C:\\Users\\hp\\Music"
                song = random.choice(os.listdir(music_dir))
                os.startfile(os.path.join(music_dir, song))
                break
            time.sleep(30)

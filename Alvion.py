import pyttsx3
import whisper
import speech_recognition as sr
import warnings
import datetime
import os
import cv2
import threading
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import sys
import pygetwindow as gw
import pyautogui
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

engine= pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#Text to speech
def speak(audio):
    engine.say(audio)
    print(f"BOT: {audio}")
    engine.runAndWait()
    
# Voice to text  
def takecommand():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                speak("I didn't hear anything.")
                return "none"

        # Save audio to a file
        try:
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())
        except Exception as e:
            speak("Sorry, I couldn't save the audio.")
            return "none"

        # Load Whisper model and transcribe
        try:
            model = whisper.load_model("base")
            print("Recognizing...") 
            result = model.transcribe("temp.wav", language="en")
            print("User:", result["text"])
            return result["text"]
        except Exception as e:
            speak("Say that again, please.")
            return "none"

    except Exception as e:
        speak("Something went wrong.")
        return "none"
    
def listen_for_wake_word(wake_words=["hey zora", "ok zora","okay zora","hey, zora","ok, zora","okay, zora"]):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for wake word...")
        while True:
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                with open("wake_temp.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                model = whisper.load_model("base")
                result = model.transcribe("wake_temp.wav", language="en")
                command = result["text"].lower()
                print("Wake Check:", command)
                for wake_word in wake_words:
                    if wake_word in command:
                        speak("Yes, I am listening.")
                        return 
            except:
                continue

#To wish
def wish():
    hour= int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning")
    elif hour>=12 and hour<16:
        speak("Good afternoon")
    else:
        speak("Good evening")
        
    speak("I am zora. How can i help you")
    
if __name__ == "__main__":
    
    while True:
        
        # listen_for_wake_word()
        query= takecommand().lower()
        
        #logic building for tasks
        
        if "open notepad" in query:
            npath= "C:\\Windows\\System32\\notepad.exe"
            os.startfile(npath)
            
        elif "close notepad" in query:
            speak("Okay sir, closing notepad")
            os.system("taskkill /f /im notepad.exe >nul 2>&1")
            
        elif "open adobe reader" in query:
            apath= "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Adobe Reader XI.lnk"
            os.startfile(apath)
            
        elif "close adobe reader" in query:
            speak("Okay sir, closing adobe reader")
            os.system("taskkill /f /im AcroRd32.exe >nul 2>&1")
            
        elif "open command prompt" in query:
            os.system("start cmd")
            
        elif "close command prompt" in query:
            speak("Okay sir, closing command prompt")
            os.system("taskkill /f /im cmd.exe >nul 2>&1")
            
        elif "open webcam" in query:
            camera_open=False
            cap=None
            if not camera_open:
                camera_open= True
                
                def webcam_thread():
                    global cap, camera_open
                    cap=cv2.VideoCapture(0)
                    while camera_open:
                        ret, img= cap.read()
                        if not ret:
                            break
                        cv2.imshow('webcam', img)
                        if cv2.waitKey(1)==27:
                            break
                    
                    cap.release()
                    cv2.destroyAllWindows()
                    camera_open= False
                    
                threading.Thread(target=webcam_thread).start()
            
        elif "close webcam" in query:
            speak("Okay sir, closing webcam")
            camera_open = False
            
        elif "play music" in query:
            music_dir= "C:\\Users\\hp\\Music"
            songs= os.listdir(music_dir)
            rd= random.choice(songs)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir, rd))
                    
        elif "close music" in query:
            speak("Okay sir, closing music")
            os.system("taskkill /f /im Microsoft.Media.Player.exe >nul 2>&1")

                    
        elif "ip address" in query:
            ip= get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")
            
        elif "wikipedia" in query or "who is" in query or "what is" in query or "tell me about" in query:
            
            speak("Searching Wikipedia...")
            for word in ["wikipedia", "who is", "what is", "tell me about"]:
               query = query.replace(word, "")
               query = query.strip()

            try:
              search_results = wikipedia.search(query)
              if search_results:
               page_title = search_results[0]
               results = wikipedia.summary(page_title, sentences=10)
               speak("According to Wikipedia...")
               speak(results)
              else:
               speak("Sorry, I couldn't find anything on Wikipedia.")
            except Exception as e:
               speak("Sorry, an error occurred.")
               print(e)
               
        elif "open youtube" in query:
            os.system('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --new-window https://www.youtube.com')
            
        elif "close youtube" in query:
            try:
                found = False
                for window in gw.getWindowsWithTitle('Youtube'):
                    if window.visible:
                        speak("Closing Youtube window")
                        window.activate()
                        pyautogui.hotkey('alt', 'f4')
                        found = True
                        break

                if not found:
                    speak("No Youtube window found")

            except Exception as e:
                speak("Something went wrong while trying to close Youtube")
                print(e)
            
        elif "open facebook" in query:
            os.system('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --new-window https://www.facebook.com')
            
        elif "close facebook" in query:
            try:
                found = False
                for window in gw.getWindowsWithTitle('Facebook'):
                    if window.visible:
                        speak("Closing Facebook window")
                        window.activate()
                        pyautogui.hotkey('alt', 'f4')
                        found = True
                        break

                if not found:
                    speak("No Facebook window found")

            except Exception as e:
                speak("Something went wrong while trying to close Facebook")
                print(e)

              
        elif "open whatsapp" in query:
            os.system("start whatsapp:")
            
        elif "close whatsapp" in query:
            speak("Okay sir, closing whatsapp")
            os.system("taskkill /f /im Whatsapp.exe >nul 2>&1")
            
        elif "open instagram" in query:
            ipath= "C:\\Users\\hp\\OneDrive\\Desktop\\Instagram.lnk"
            os.startfile(ipath)
            
        elif "close instagram" in query:
            try:
                found = False
                for window in gw.getWindowsWithTitle('Instagram'):
                    if window.visible:
                        speak("Closing instagram window")
                        window.activate()
                        pyautogui.hotkey('alt', 'f4')
                        found = True
                        break

                if not found:
                    speak("No instagram window found")

            except Exception as e:
                speak("Something went wrong while trying to close instagram")
                print(e)

            
        elif "open google chrome" in query:
            speak("Sir, What should i search on google chrome")
            cm= takecommand().lower()
            chrome_path= "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
            webbrowser.get('chrome').open(f"https://www.google.com/search?q={cm}")
        
        elif "close google chrome" in query:
            speak("Okay sir, closing google chrome")
            os.system("taskkill /f /im chrome.exe >nul 2>&1")

        elif "play video on youtube" in query:
            speak("Sir, What should i play on youtube")
            cm= takecommand().lower()
            kit.playonyt(cm)  
            
        elif "set alarm" in query:
            speak("Tell hours")
            hour= int(takecommand().lower())
            speak("Tell minutes")
            minute= int(takecommand().lower())
            list=[hour,minute]
            if list: 
                music_dir= "C:\\Users\\hp\\Music"
                songs= os.listdir(music_dir)
                os.startfile(os.path.join(music_dir,songs[0]))            
            
        elif "stop" in query or "thanks" in query:
            speak("Thanks for using me sir")
            sys.exit()
            
        speak("Sir, do you have any other work")
        


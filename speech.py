import pyttsx3
import speech_recognition as sr
from faster_whisper import WhisperModel

class Speech_handler:
    
    def __init__(self):
        # Text-to-Speech setup
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)

        # Load Faster-Whisper model (runs smoothly on CPU/Windows)
        self.model = WhisperModel("base", device="cpu", compute_type="int8")

    # ---------------- TEXT TO SPEECH ---------------- #
    def speak(self, audio):
        self.engine.say(audio)
        print(f"BOT: {audio}")
        self.engine.runAndWait()

    # ---------------- SPEECH TO TEXT ---------------- #
    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 0.8
            audio = r.listen(source, timeout=5, phrase_time_limit=6)

        # Try Google first (FAST)
        try:
            query = r.recognize_google(audio).lower()
            print("User:", query)
            return query
        except Exception:
            pass

        # Fallback to Whisper (ROBUST)
        try:
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())

            print("Recognizing with Whisper...")
            segments, info = self.model.transcribe("temp.wav", language="en")
            text = " ".join([segment.text for segment in segments]).strip().lower()
            
            print("User (Whisper):", text)
            return text if text else "none"
        except Exception as e:
            print("Error:", e)
            self.speak("Say that again please")
            return "none"
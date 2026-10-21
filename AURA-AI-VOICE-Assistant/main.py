import speech_recognition as sr
import pyttsx3


# -------------------------
# Text-to-Speech
# -------------------------

engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(text):
    print("AURA:", text)
    engine.say(text)
    engine.runAndWait()


# -------------------------
# Speech Recognition
# -------------------------

recognizer = sr.Recognizer()


# -------------------------
# Start AURA
# -------------------------

speak("Hello Devu, I am AURA.")
speak("Please say something.")

speak("Hello Devu, I am AURA.")
speak("Please say something.")

with sr.Microphone() as source:
    print("Adjusting for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Listening...")
    audio = recognizer.listen(source)

print("Processing...")

try:
    text = recognizer.recognize_google(audio)

    print("You:", text)

    speak("I heard you.")

except sr.UnknownValueError:
    speak("Sorry, I could not understand you.")

except sr.RequestError:
    speak("Sorry, I am having trouble connecting to the speech recognition service.")


print("Processing...")


try:
    text = recognizer.recognize_google(audio)

    print("You:", text)

    speak("I heard you.")

except sr.UnknownValueError:
    speak("Sorry, I could not understand you.")

except sr.RequestError:
    speak("Sorry, I am having trouble connecting to the speech recognition service.")
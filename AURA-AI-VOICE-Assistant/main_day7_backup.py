import os
import webbrowser
import datetime
import speech_recognition as sr
import pyttsx3

from dotenv import load_dotenv
from google import genai


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env")
    print("Please add your Gemini API key to the .env file.")
    raise SystemExit


# Gemini client
client = genai.Client(api_key=API_KEY)


# =========================================================
# TEXT TO SPEECH
# =========================================================

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text):
    """Make AURA speak."""
    
    if not text:
        return

    print(f"AURA: {text}")

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS Error:", e)


# =========================================================
# LISTEN
# =========================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.non_speaking_duration = 0.5


def listen():
    """Listen to microphone and return text."""

    with sr.Microphone() as source:

        print("\nAdjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=0.7)

        print("Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=12
            )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    print("Processing...")

    try:
        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        text = text.strip()

        print(f"You: {text}")

        return text

    except sr.UnknownValueError:
        print("Could not understand speech.")
        return ""

    except sr.RequestError as e:
        print("Speech recognition error:", e)
        return ""


# =========================================================
# EXIT DETECTION
# =========================================================

def is_exit_command(command):
    """
    Detect exit commands anywhere inside the sentence.

    Examples:
        exit
        now exit
        please exit
        exit now
        quit
        please stop
        goodbye
    """

    command = command.lower().strip()

    exit_words = [
        "exit",
        "quit",
        "stop",
        "goodbye",
        "bye"
    ]

    for word in exit_words:

        if word in command.split():
            return True

    return False


# =========================================================
# LOCAL COMMANDS
# =========================================================

def handle_local_command(command):
    """
    Handle commands that should NOT go to Gemini.

    Returns:
        response, handled
    """

    command = command.lower().strip()


    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    time_words = [
        "what time is it",
        "what is the time",
        "tell me the time",
        "current time",
        "time please"
    ]

    if any(x in command for x in time_words):

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}.", True


    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    date_words = [
        "what is today's date",
        "what date is it",
        "today's date",
        "current date"
    ]

    if any(x in command for x in date_words):

        today = datetime.datetime.now().strftime("%A, %d %B %Y")

        return f"Today is {today}.", True


    # -----------------------------------------------------
    # YOUTUBE
    # -----------------------------------------------------

    if "open youtube" in command:

        webbrowser.open("https://www.youtube.com")

        return "Opening YouTube.", True


    # -----------------------------------------------------
    # GOOGLE
    # -----------------------------------------------------

    if "open google" in command:

        webbrowser.open("https://www.google.com")

        return "Opening Google.", True


    # -----------------------------------------------------
    # GITHUB
    # -----------------------------------------------------

    if "open github" in command:

        webbrowser.open("https://github.com")

        return "Opening GitHub.", True


    return "", False


# =========================================================
# GEMINI
# =========================================================

def ask_gemini(command):

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=command
        )

        if response and response.text:

            return response.text.strip()

        return "Sorry, I could not generate a response."

    except Exception as e:

        print("\nGemini Error:")
        print(e)

        return "Sorry, I am having trouble connecting to Gemini right now."


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 60)
    print("AURA - Personal Voice Assistant")
    print("=" * 60)

    speak(
        "I am AURA, your personal voice assistant. "
        "How can I help you?"
    )


    while True:

        try:

            # ---------------------------------------------
            # LISTEN
            # ---------------------------------------------

            command = listen()

            if not command:
                continue


            # ---------------------------------------------
            # EXIT CHECK
            #
            # IMPORTANT:
            # This happens BEFORE Gemini.
            # ---------------------------------------------

            if is_exit_command(command):

                speak("Goodbye, Devu. See you soon.")

                print("\nAURA stopped.")

                break


            # ---------------------------------------------
            # LOCAL COMMANDS
            # ---------------------------------------------

            response, handled = handle_local_command(command)

            if handled:

                speak(response)

                continue


            # ---------------------------------------------
            # GEMINI
            # ---------------------------------------------

            response = ask_gemini(command)

            speak(response)


        except KeyboardInterrupt:

            print("\n\nAURA stopped by keyboard.")

            break


        except Exception as e:

            print("\nUnexpected Error:")
            print(e)

            speak("Something went wrong, but I am still running.")


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":
    main()
import os
import webbrowser
import datetime
import speech_recognition as sr
import pyttsx3

from dotenv import load_dotenv
from google import genai
from google.genai import types


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:

    print("ERROR: GEMINI_API_KEY not found in .env")
    print("Please add your Gemini API key to the .env file.")

    raise SystemExit


# =========================================================
# GEMINI CLIENT
# =========================================================

# Keep Gemini from blocking AURA indefinitely.
# SDK timeout values are in milliseconds; one attempt avoids long retry loops.
client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=20000,
        retry_options=types.HttpRetryOptions(attempts=1)
    )
)


# =========================================================
# TEXT TO SPEECH
# =========================================================

def speak(text):
    """
    Make AURA speak reliably.
    """

    if not text:
        return

    print(f"AURA: {text}")

    try:

        # -------------------------------------------------
        # Remove Gemini formatting
        # -------------------------------------------------

        text = text.replace("**", "")
        text = text.replace("*", "")
        text = text.replace("#", "")
        text = text.replace("`", "")
        text = text.replace("_", "")

        text = " ".join(text.split())


        # -------------------------------------------------
        # Create fresh TTS engine
        # -------------------------------------------------

        voice_engine = pyttsx3.init()

        voice_engine.setProperty(
            "rate",
            170
        )

        voice_engine.setProperty(
            "volume",
            1.0
        )

        voice_engine.say(text)

        voice_engine.runAndWait()

        voice_engine.stop()


    except Exception as e:

        print("TTS Error:")
        print(e)


# =========================================================
# SPEECH RECOGNITION
# =========================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300

recognizer.dynamic_energy_threshold = True

recognizer.pause_threshold = 1.5

recognizer.non_speaking_duration = 0.8


def listen():
    """
    Listen to microphone and return recognized text.
    """

    with sr.Microphone() as source:

        print("\nListening...")
        print("Speak your complete command...")

        try:

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=20
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

        print("Speech recognition error:")

        print(e)

        return ""


# =========================================================
# EXIT DETECTION
# =========================================================

def is_exit_command(command):
    """
    Check whether the user wants to exit AURA.
    """

    command = command.lower().strip()


    exit_commands = [
        "exit",
        "quit",
        "goodbye",
        "bye"
    ]


    # Exact command

    if command in exit_commands:

        return True


    # Commands like:
    # bye aura
    # exit aura
    # goodbye aura

    for word in exit_commands:

        if command.startswith(word + " "):

            return True


    return False


# =========================================================
# LOCAL COMMANDS
# =========================================================

def handle_local_command(command):
    """
    Handle commands that should be executed locally.

    Returns:
        response, handled
    """

    command = command.lower().strip()


    # =====================================================
    # WINDOWS APPLICATIONS
    # =====================================================

    # -----------------------------------------------------
    # CALCULATOR
    # -----------------------------------------------------

    if (
        "open calculator" in command
        or "calculator open" in command
        or command == "calculator"
    ):

        os.system("start calc")

        return (
            "Opening Calculator.",
            True
        )


    # -----------------------------------------------------
    # NOTEPAD
    # -----------------------------------------------------

    if (
        "open notepad" in command
        or "notepad open" in command
        or command == "notepad"
    ):

        os.system("start notepad")

        return (
            "Opening Notepad.",
            True
        )


    # -----------------------------------------------------
    # PAINT
    # -----------------------------------------------------

    if (
        "open paint" in command
        or "paint open" in command
        or command == "paint"
    ):

        os.system("start mspaint")

        return (
            "Opening Paint.",
            True
        )


    # =====================================================
    # WINDOWS FOLDERS
    # =====================================================

    # -----------------------------------------------------
    # DOWNLOADS
    # -----------------------------------------------------

    if (
        "open downloads" in command
        or "open download" in command
        or "downloads open" in command
        or "download open" in command
        or command == "downloads"
        or command == "download"
    ):

        downloads_path = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )


        if os.path.exists(downloads_path):

            os.startfile(
                downloads_path
            )

            return (
                "Opening Downloads.",
                True
            )


        return (
            "I could not find the Downloads folder.",
            True
        )


    # -----------------------------------------------------
    # DOCUMENTS
    # -----------------------------------------------------

    if (
        "open documents" in command
        or "open document" in command
        or "documents open" in command
        or "document open" in command
        or command == "documents"
        or command == "document"
    ):

        documents_path = os.path.join(
            os.path.expanduser("~"),
            "Documents"
        )


        if os.path.exists(documents_path):

            os.startfile(
                documents_path
            )

            return (
                "Opening Documents.",
                True
            )


        return (
            "I could not find the Documents folder.",
            True
        )


    # -----------------------------------------------------
    # DESKTOP
    # -----------------------------------------------------

    if (
        "open desktop" in command
        or "desktop open" in command
        or command == "desktop"
    ):

        desktop_path = os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        )


        if os.path.exists(desktop_path):

            os.startfile(
                desktop_path
            )

            return (
                "Opening Desktop.",
                True
            )


        return (
            "I could not find the Desktop folder.",
            True
        )


    # =====================================================
    # VOLUME CONTROL
    # =====================================================

    # -----------------------------------------------------
    # VOLUME UP
    # -----------------------------------------------------

    if (
        "volume up" in command
        or "increase volume" in command
        or "increase the volume" in command
        or "turn up volume" in command
        or "volume increase" in command
        or "louder" in command
        or command == "increase"
    ):

        try:

            from pycaw.pycaw import AudioUtilities

            # Current pycaw returns an AudioDevice; use its EndpointVolume.
            devices = AudioUtilities.GetSpeakers()
            volume = devices.EndpointVolume


            current_volume = (
                volume.GetMasterVolumeLevelScalar()
            )


            amount = 0.10


            numbers = [
                word
                for word in command.split()
                if word.isdigit()
            ]


            if numbers:

                amount = (
                    int(numbers[0]) / 100
                )


            new_volume = min(
                1.0,
                current_volume + amount
            )


            volume.SetMasterVolumeLevelScalar(
                new_volume,
                None
            )


            percentage = int(
                new_volume * 100
            )


            return (
                f"Volume increased to "
                f"{percentage} percent.",
                True
            )


        except Exception as e:

            print("Volume Error:")
            print(e)

            return (
                "I could not change the volume.",
                True
            )


    # -----------------------------------------------------
    # VOLUME DOWN
    # -----------------------------------------------------

    if (
        "volume down" in command
        or "decrease volume" in command
        or "decrease the volume" in command
        or "turn down volume" in command
        or "volume decrease" in command
        or "lower volume" in command
        or command == "decrease"
    ):

        try:

            from pycaw.pycaw import AudioUtilities

            # Current pycaw returns an AudioDevice; use its EndpointVolume.
            devices = AudioUtilities.GetSpeakers()
            volume = devices.EndpointVolume


            current_volume = (
                volume.GetMasterVolumeLevelScalar()
            )


            amount = 0.10


            numbers = [
                word
                for word in command.split()
                if word.isdigit()
            ]


            if numbers:

                amount = (
                    int(numbers[0]) / 100
                )


            new_volume = max(
                0.0,
                current_volume - amount
            )


            volume.SetMasterVolumeLevelScalar(
                new_volume,
                None
            )


            percentage = int(
                new_volume * 100
            )


            return (
                f"Volume decreased to "
                f"{percentage} percent.",
                True
            )


        except Exception as e:

            print("Volume Error:")
            print(e)

            return (
                "I could not change the volume.",
                True
            )


    # =====================================================
    # MUTE
    # =====================================================

    if (
        "mute" in command
        and "unmute" not in command
    ):

        try:

            from pycaw.pycaw import AudioUtilities

            # Current pycaw returns an AudioDevice; use its EndpointVolume.
            devices = AudioUtilities.GetSpeakers()
            volume = devices.EndpointVolume


            volume.SetMute(
                1,
                None
            )


            return (
                "Volume muted.",
                True
            )


        except Exception as e:

            print("Mute Error:")
            print(e)

            return (
                "I could not mute the volume.",
                True
            )


    # =====================================================
    # UNMUTE
    # =====================================================

    if "unmute" in command:

        try:

            from pycaw.pycaw import AudioUtilities

            # Current pycaw returns an AudioDevice; use its EndpointVolume.
            devices = AudioUtilities.GetSpeakers()
            volume = devices.EndpointVolume


            volume.SetMute(
                0,
                None
            )


            return (
                "Volume unmuted.",
                True
            )


        except Exception as e:

            print("Unmute Error:")
            print(e)

            return (
                "I could not unmute the volume.",
                True
            )


    # =====================================================
    # SET VOLUME
    # =====================================================

    if (
        "set volume" in command
        or "volume to" in command
        or "volume at" in command
    ):

        try:

            from pycaw.pycaw import AudioUtilities

            # Current pycaw returns an AudioDevice; use its EndpointVolume.
            devices = AudioUtilities.GetSpeakers()
            volume = devices.EndpointVolume


            numbers = [
                word
                for word in command.split()
                if word.isdigit()
            ]


            if not numbers:

                return (
                    "Please tell me the volume percentage.",
                    True
                )


            percentage = int(
                numbers[0]
            )


            percentage = max(
                0,
                min(100, percentage)
            )


            volume.SetMasterVolumeLevelScalar(
                percentage / 100,
                None
            )


            return (
                f"Volume set to "
                f"{percentage} percent.",
                True
            )


        except Exception as e:

            print("Set Volume Error:")
            print(e)

            return (
                "I could not set the volume.",
                True
            )


    # =====================================================
    # LOCK COMPUTER
    # =====================================================

    if (
        "lock pc" in command
        or "lock computer" in command
        or "lock my pc" in command
        or "lock my computer" in command
    ):

        os.system(
            "rundll32.exe "
            "user32.dll,LockWorkStation"
        )

        return (
            "Locking your computer.",
            True
        )


    # =====================================================
    # TIME
    # =====================================================

    time_words = [

        "what time is it",

        "what is the time",

        "tell me the time",

        "current time",

        "time please"

    ]


    if any(
        word in command
        for word in time_words
    ):

        current_time = (
            datetime.datetime.now().strftime(
                "%I:%M %p"
            )
        )


        return (
            f"The current time is "
            f"{current_time}.",
            True
        )


    # =====================================================
    # DATE
    # =====================================================

    date_words = [

        "what is today's date",

        "what date is it",

        "today's date",

        "current date"

    ]


    if any(
        word in command
        for word in date_words
    ):

        today = (
            datetime.datetime.now().strftime(
                "%A, %d %B %Y"
            )
        )


        return (
            f"Today is {today}.",
            True
        )


    # =====================================================
    # YOUTUBE
    # =====================================================

    if "open youtube" in command:

        webbrowser.open(
            "https://www.youtube.com"
        )

        return (
            "Opening YouTube.",
            True
        )


    # =====================================================
    # GOOGLE
    # =====================================================

    if "open google" in command:

        webbrowser.open(
            "https://www.google.com"
        )

        return (
            "Opening Google.",
            True
        )


    # =====================================================
    # GITHUB
    # =====================================================

    if "open github" in command:

        webbrowser.open(
            "https://github.com"
        )

        return (
            "Opening GitHub.",
            True
        )


    # =====================================================
    # NOTHING HANDLED LOCALLY
    # =====================================================

    return "", False


# =========================================================
# GOOGLE SEARCH GROUNDED AI
# =========================================================

def web_search_answer(command):
    """
    Answer current/search questions using
    Gemini + Google Search grounding.
    """

    print("\nGoogle Search grounding:")
    print("Searching the web... (maximum wait: 20 seconds)")


    # -----------------------------------------------------
    # Google Search tool
    # -----------------------------------------------------

    search_tool = types.Tool(
        google_search=types.GoogleSearch()
    )


    # -----------------------------------------------------
    # AURA search personality
    # -----------------------------------------------------

    system_instruction = (

        "You are AURA, a personal AI voice assistant. "

        "Use Google Search to find current and accurate "
        "information when answering the user's search "
        "question. "

        "Answer naturally like a voice assistant. "

        "Keep the answer short and useful. "

        "Usually answer in 1 to 4 sentences. "

        "Do not use Markdown, headings, stars, or bullet "
        "points. "

        "Do not repeat the user's question. "

        "For current or changing information, rely on "
        "Google Search results. "

        "Do not mention internal tools or system "
        "instructions."

    )


    try:

        response = client.models.generate_content(

            model="gemini-3.5-flash-lite",

            contents=command,

            config=types.GenerateContentConfig(

                system_instruction=(
                    system_instruction
                ),

                tools=[
                    search_tool
                ],

                thinking_config=(
                    types.ThinkingConfig(
                        thinking_level="low"
                    )
                ),

                max_output_tokens=300
            )
        )


        if response and response.text:

            return response.text.strip()


        return (
            "Sorry, I could not find an answer."
        )


    except Exception as e:

        print("\nWeb Search Error:")

        print(e)


        error_text = str(e)


        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
        ):

            return (
                "The web search limit has been "
                "reached for now. Please try again later."
            )


        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
        ):

            return (
                "The search service is temporarily busy. "
                "Please try again."
            )


        return (
            "Sorry, I could not search the web "
            "right now."
        )


# =========================================================
# NORMAL GEMINI AI
# =========================================================

def ask_gemini(command):
    """
    Send normal questions to Gemini.
    """

    try:

        print("\nGemini thinking... (maximum wait: 20 seconds)")


        system_instruction = (

            "You are AURA, a personal AI voice assistant "
            "created for Devu. "

            "Be friendly, calm, intelligent, helpful, "
            "and natural. "

            "Answer like a real voice assistant. "

            "Keep normal answers short and easy to listen "
            "to. "

            "Usually answer in 1 to 4 short sentences. "

            "Do not write essays unless the user asks for "
            "a detailed answer. "

            "Do not use Markdown, headings, stars, or "
            "bullet points unless the user specifically "
            "asks for them. "

            "Do not repeat the user's question. "

            "For simple questions, answer directly. "

            "For technical questions, explain clearly "
            "but stay concise."

        )


        response = client.models.generate_content(

            model="gemini-3.8-flash",

            contents=command,

            config=types.GenerateContentConfig(

                system_instruction=(
                    system_instruction
                ),

                thinking_config=(
                    types.ThinkingConfig(
                        thinking_level="low"
                    )
                ),

                max_output_tokens=300
            )
        )


        if response and response.text:

            return response.text.strip()


        return (
            "Sorry, I could not generate a response."
        )


    except Exception as e:

        print("\nGemini Error:")

        print(e)


        error_text = str(e)


        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
        ):

            return (
                "Gemini has reached its current usage "
                "limit. Please try again later."
            )


        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
        ):

            return (
                "Gemini is temporarily busy. "
                "Please try again."
            )


        return (
            "Sorry, I am having trouble connecting "
            "to Gemini."
        )


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    print("=" * 60)

    print(
        "AURA - Personal Voice Assistant (Updated Volume Control)"
    )

    print("=" * 60)


    # =====================================================
    # MICROPHONE CALIBRATION
    # =====================================================

    print(
        "\nPreparing microphone..."
    )


    try:

        with sr.Microphone() as source:

            print(
                "Please stay quiet for a moment..."
            )


            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )


            print(
                "Microphone ready."
            )


    except Exception as e:

        print(
            "Microphone calibration error:"
        )

        print(e)


    # =====================================================
    # STARTUP MESSAGE
    # =====================================================

    speak(
        "I am AURA, your personal voice assistant. "
        "How can I help you?"
    )


    # =====================================================
    # MAIN LOOP
    # =====================================================

    while True:

        try:

            # -------------------------------------------------
            # LISTEN
            # -------------------------------------------------

            command = listen()


            if not command:

                continue


            # -------------------------------------------------
            # EXIT
            # -------------------------------------------------

            if is_exit_command(command):

                speak(
                    "Goodbye, Devu. See you soon."
                )


                print(
                    "\nAURA stopped."
                )


                break


            # =================================================
            # GOOGLE SEARCH
            # =================================================
            #
            # IMPORTANT:
            # Search is checked BEFORE local commands.
            #
            # Example:
            # "search latest AI news"
            # "search today's weather in Bhopal"
            # "search who won the match"
            #
            # These go to Google Search grounding.
            # =================================================

            if (
                command.lower().startswith(
                    "search "
                )

                or command.lower().startswith(
                    "search for "
                )

                or command.lower().startswith(
                    "google search "
                )
            ):

                response = web_search_answer(
                    command
                )


                speak(
                    response
                )


                continue


            # =================================================
            # LOCAL COMMANDS
            # =================================================

            response, handled = (
                handle_local_command(
                    command
                )
            )


            if handled:

                speak(
                    response
                )


                continue


            # =================================================
            # NORMAL GEMINI
            # =================================================

            response = ask_gemini(
                command
            )


            speak(
                response
            )


        # =====================================================
        # KEYBOARD INTERRUPT
        # =====================================================

        except KeyboardInterrupt:

            print(
                "\n\nAURA stopped by keyboard."
            )

            break


        # =====================================================
        # UNEXPECTED ERROR
        # =====================================================

        except Exception as e:

            print(
                "\nUnexpected Error:"
            )

            print(e)


            speak(
                "Something went wrong, "
                "but I am still running."
            )


# =========================================================
# START AURA
# =========================================================

if __name__ == "__main__":

    main()
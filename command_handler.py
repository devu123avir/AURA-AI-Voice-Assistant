import webbrowser
import datetime
from urllib.parse import quote


def handle_command(command, speak):

    # ==========================================
    # CLEAN COMMAND
    # ==========================================

    command = command.lower().strip()

    if not command:
        return None

    # ==========================================
    # EXIT AURA
    # ==========================================

    exit_commands = [
        "exit",
        "quit",
        "stop",
        "goodbye",
        "exit aura",
        "quit aura",
        "goodbye aura",
        "close aura",
        "stop aura"
    ]

    if command in exit_commands:
        speak("Goodbye Devu. See you soon.")
        return False

    # ==========================================
    # OPEN YOUTUBE
    # ==========================================

    youtube_commands = [
        "open youtube",
        "open up youtube",
        "take me to youtube",
        "youtube kholo",
        "i want to watch youtube",
        "can you open youtube",
        "show me youtube",
        "go to youtube",
        "youtube open karo"
    ]

    if any(phrase in command for phrase in youtube_commands):

        speak("Opening YouTube.")

        webbrowser.open(
            "https://www.youtube.com"
        )

        return True

    # ==========================================
    # OPEN GOOGLE
    # ==========================================

    google_commands = [
        "open google",
        "open up google",
        "take me to google",
        "google kholo",
        "can you open google",
        "show me google",
        "go to google",
        "google open karo"
    ]

    if any(phrase in command for phrase in google_commands):

        speak("Opening Google.")

        webbrowser.open(
            "https://www.google.com"
        )

        return True

    # ==========================================
    # CURRENT TIME
    # ==========================================

    time_commands = [
        "what time is it",
        "what is the time",
        "what's the time",
        "tell me the time",
        "tell me current time",
        "what is current time",
        "what's current time",
        "current time",
        "time please",
        "can you tell me the time"
    ]

    if any(phrase in command for phrase in time_commands):

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        speak(
            f"The current time is {current_time}."
        )

        return True

    # ==========================================
    # GOOGLE SEARCH
    # ==========================================

    search_triggers = [
        "search for ",
        "search ",
        "google search ",
        "find ",
        "look for ",
        "look up "
    ]

    for trigger in search_triggers:

        if command.startswith(trigger):

            search_query = command[len(trigger):].strip()

            if search_query:

                speak(
                    f"Searching for {search_query}."
                )

                search_url = (
                    "https://www.google.com/search?q="
                    + quote(search_query)
                )

                webbrowser.open(search_url)

                return True

            else:

                speak(
                    "What should I search for?"
                )

                return True

    # ==========================================
    # NO BASIC COMMAND FOUND
    # SEND TO GEMINI
    # ==========================================

    return None
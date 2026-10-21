# 🤖 AURA — AI Voice Assistant

**AURA** is a Python-based AI voice assistant designed to make everyday computer tasks easier through voice commands. It combines speech recognition, AI-powered responses, web search, and Windows automation in one application.

## ✨ Features

* 🎤 **Voice Recognition:** Listens to and recognizes spoken commands.
* 🧠 **AI-Powered Responses:** Uses Google's Gemini API to answer questions.
* 🔎 **Web Search:** Helps retrieve information from Google Search.
* 💻 **Windows Automation:** Opens applications such as Calculator, Notepad, and Paint.
* 🔊 **Text-to-Speech:** Responds to users with spoken answers.
* 🎚️ **System Controls:** Supports volume control and locking the computer.
* 🌐 **Quick Website Access:** Opens websites such as YouTube, Google, and GitHub.
* 📅 **Time and Date:** Provides the current date and time through voice commands.

## 🛠️ Technologies Used

* Python
* Google Gemini API
* SpeechRecognition
* pyttsx3
* Python-dotenv
* Pycaw
* Web Browser Automation

## 📋 Requirements

* Windows computer
* Python 3
* Internet connection
* Google Gemini API key
* Microphone and speakers

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/devu123avir/AURA-AI-Voice-Assistant.git
```

### 2. Open the project folder

```bash
cd AURA-AI-Voice-Assistant
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

Install the Python packages required by the project:

```bash
pip install google-genai python-dotenv SpeechRecognition pyttsx3 PyAudio pycaw
```

If a package is already installed, pip will handle it normally.

### 6. Configure your API key

Create a `.env` file in the project root and add:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key. **Never upload your real API key to GitHub.**

### 7. Run AURA

```bash
python main.py
```

## 🔐 Security

* API keys are stored in a local `.env` file.
* The `.env` file should not be committed to GitHub.
* Never share your API key publicly.

## ⚠️ Notes

* AURA requires an active internet connection for online AI and search features.
* Gemini API availability and usage limits may affect responses.
* Microphone access and compatible audio dependencies are required for voice interaction.
* Some Windows-specific features may require additional permissions or dependencies.

## 🔮 Future Improvements

* Improved speech recognition accuracy
* More natural conversations
* Custom wake-word detection
* Additional Windows automation commands
* A graphical user interface
* Better error handling and response reliability

## 👨‍💻 Author

**Devu (@devu123avir)**

## 📄 License

A license has not yet been specified for this project.

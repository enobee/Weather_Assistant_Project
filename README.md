# Weather AI Assistant

## 🌤 Overview
The **Weather AI Assistant** is a Python-based AI agent that provides users with real-time weather information and clothing recommendations based on weather conditions.



## 🛠 Installation
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/enobee/Weather_Assistant_Project.git
cd Weather_Assistant_Project
```

### 2️⃣ Set Up a Virtual Environment
```sh
python -m venv weather_assistant_env
source weather_assistant_env/bin/activate  # On macOS/Linux
weather_assistant_env\Scripts\activate    # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

## 🔑 API Keys Setup
Create a `.env` file in the root directory and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key
OPENWEATHER_API_KEY=your_weather_api_key
```

## 🚀 Running the AI Assistant
```sh
python weather_assistant.py
```

## 📝 Usage
- Ask for weather updates: *"What's the weather like in New York?"*
- Get clothing recommendations based on weather: *"What should I wear in London today?"*
- Type `exit` to close the assistant.

## 🛠 Troubleshooting
- **Missing API keys?** Ensure `.env` is properly configured.
- **Installation issues?** Run `pip install -r requirements.txt`.
- **Git not tracking files?** Run `git status` to check ignored files.

## 📜 License
This project is licensed under the MIT License.


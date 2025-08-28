# 🎙️ ARIA - Advanced Voice Assistant

**Professional Voice Assistant with Elegant Interface**

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Features

### 🎯 Core Functions
- **🗣️ Natural Speech Recognition** - Understands your voice commands clearly
- **🤖 Intelligent Text-to-Speech** - Responds with natural voice
- **📅 Schedule Management** - Track your daily appointments
- **👥 Contact Management** - Quick access to your contacts
- **🌤️ Weather Information** - Real-time weather updates
- **🔍 Web Search** - Instant Google searches
- **🧮 Smart Calculator** - Voice-controlled calculations
- **📊 System Monitoring** - Check your computer's performance

### 🎨 Professional Interface
- **Beautiful Console Output** - Color-coded responses
- **Real-time Visual Feedback** - See what's happening
- **Session Statistics** - Track your usage
- **Elegant Animations** - Smooth user experience

### 🔧 Advanced Capabilities
- **Auto-calibration** - Optimizes for your microphone
- **Smart Command Processing** - Understands natural language
- **Error Recovery** - Gracefully handles problems
- **Data Persistence** - Saves your preferences and data

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd "Voice Virtual Assistant"

# Install dependencies
pip install speechrecognition pyttsx3 pyaudio python-dotenv requests psutil rich
```

### 2. Setup Configuration

Create a `.env` file:
```env
# Weather API (optional - get free key from OpenWeatherMap)
WEATHER_API_KEY=your_weather_api_key_here

# OpenAI API (optional - for future AI features)
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run ARIA

```bash
python aria_voice_assistant.py
```

## 🎤 How to Use

### Voice Commands

| Category | Examples | Description |
|----------|----------|-------------|
| **🗣️ Greetings** | "Hello", "Hi ARIA", "Good morning" | Start conversation |
| **⏰ Time & Date** | "What time is it?", "What's the date?" | Get current time/date |
| **📅 Schedule** | "What's my schedule?", "Any meetings?" | View appointments |
| **🌤️ Weather** | "How's the weather?", "Weather in Tokyo" | Get weather info |
| **🔍 Search** | "Search for Python tutorials" | Open web search |
| **🧮 Calculator** | "Calculate 25 times 4", "What's 100 plus 50?" | Perform calculations |
| **📊 System** | "System status", "Computer performance" | Check system info |
| **👥 Contacts** | "Call Egi", "Contact Sophie" | Find contact info |
| **🚪 Exit** | "Goodbye", "Quit", "Exit" | Stop the assistant |

### Tips for Best Results
- 🎯 **Speak clearly** and at normal pace
- 🎤 **Use good microphone** for better recognition
- 🔇 **Minimize background noise**
- 🗣️ **Use natural language** - no need for rigid commands

## 📁 Project Structure

```
Voice Virtual Assistant/
├── 📄 aria_voice_assistant.py    # Main application
├── 📄 .env                       # Configuration (create this)
├── 📄 README.md                  # This documentation
├── 📋 schedule.json             # Your appointments (auto-created)
├── 📞 contacts.json             # Your contacts (auto-created)
└── 📊 conversation_history.json # Chat history (auto-created)
```

## 🎨 Customization

### Personalize Your Assistant

Edit these variables in `aria_voice_assistant.py`:

```python
self.user_name = "Your Name"           # Your name
self.assistant_name = "ARIA"           # Assistant name
self.config = {
    "voice_rate": 180,                 # Speech speed (150-200)
    "voice_volume": 0.9,               # Volume (0.0-1.0)
    "listen_timeout": 5,               # Listening timeout (seconds)
}
```

### Add Custom Schedule

Edit `schedule.json`:
```json
[
  {
    "time": "09:00",
    "title": "Team Meeting",
    "location": "Conference Room",
    "priority": "high"
  }
]
```

### Add Custom Contacts

Edit `contacts.json`:
```json
{
  "john": {
    "name": "John Doe",
    "phone": "+1-555-0123",
    "email": "john@example.com"
  }
}
```

## 🔧 Troubleshooting

### Common Issues

**🎤 Microphone not working:**
```bash
# Test microphone access
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

**🔊 No speech output:**
- Check system volume
- Verify speakers/headphones connection
- Try different TTS voice

**🌐 Speech recognition errors:**
- Check internet connection (uses Google API)
- Ensure microphone permissions
- Try speaking more clearly

**📦 Import errors:**
```bash
# Reinstall dependencies
pip install --upgrade speechrecognition pyttsx3 pyaudio
```

### Performance Optimization

- **CPU Usage:** Close other audio applications
- **Memory Usage:** Restart ARIA periodically for long sessions
- **Recognition Accuracy:** Use external microphone for better quality

## 🔮 Future Features

### Planned Enhancements
- 🤖 **AI Chat Integration** (OpenAI/Claude)
- 🏠 **Smart Home Control** (Lights, AC, etc.)
- 📱 **Mobile App Integration**
- 🌍 **Multi-language Support**
- 🔐 **Voice Authentication**
- 📧 **Email Management**
- 🎵 **Advanced Media Control**
- 📝 **Note Taking & Reminders**

### Contributing
- 🐛 **Bug Reports:** Please create an issue
- 💡 **Feature Requests:** Share your ideas
- 🔧 **Pull Requests:** Contributions welcome!

## 📞 Support

Need help? Here are your options:

- 📖 **Documentation:** Read this README thoroughly
- 🐛 **Issues:** Create a GitHub issue
- 💬 **Discussions:** Join project discussions
- 📧 **Contact:** Reach out to the developer

## � License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Speech Recognition:** Google Speech API
- **Text-to-Speech:** System TTS engines
- **Weather Data:** OpenWeatherMap API
- **UI Framework:** Rich Console Library

---

**Made with ❤️ by Dian | ARIA v2.0.0**

*"Your intelligent voice companion for daily tasks"*

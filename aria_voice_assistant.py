"""
ARIA - Advanced Responsive Intelligence Assistant
Professional Voice Assistant with Elegant Interface
Version 2.0.0 - Created by Dian
"""

import os
import sys
import time
import json
import datetime
import webbrowser
import threading
from pathlib import Path
from typing import Dict, List, Optional

# Voice and Speech Libraries with error handling
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    print("Warning: speech_recognition not installed. Run: pip install speechrecognition")
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    print("Warning: pyttsx3 not installed. Run: pip install pyttsx3")
    TTS_AVAILABLE = False
    pyttsx3 = None

# Environment and HTTP
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    print("Warning: python-dotenv not installed. Run: pip install python-dotenv")
    DOTENV_AVAILABLE = False
    def load_dotenv():
        pass

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    print("Warning: requests not installed. Run: pip install requests")
    REQUESTS_AVAILABLE = False
    requests = None
# Console colors and formatting
class Colors:
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

# Load environment variables
load_dotenv()

class AriaAssistant:
    """
    ARIA - Advanced Responsive Intelligence Assistant
    Professional Voice Assistant with Elegant Features
    """
    
    def __init__(self):
        # Check required dependencies
        if not SPEECH_RECOGNITION_AVAILABLE:
            print(f"{Colors.RED}❌ Speech Recognition not available. Please install: pip install speechrecognition{Colors.END}")
            sys.exit(1)
        
        if not TTS_AVAILABLE:
            print(f"{Colors.RED}❌ Text-to-Speech not available. Please install: pip install pyttsx3{Colors.END}")
            sys.exit(1)
        
        self.user_name = "Dian"
        self.assistant_name = "ARIA"
        self.version = "2.0.0"
        self.is_listening = False
        self.is_speaking = False
        self.conversation_count = 0
        self.session_start_time = datetime.datetime.now()
        
        # Configuration
        self.config = {
            "voice_rate": 180,
            "voice_volume": 0.9,
            "listen_timeout": 5,
            "weather_api_key": os.getenv("WEATHER_API_KEY", "") if DOTENV_AVAILABLE else "",
            "openai_api_key": os.getenv("OPENAI_API_KEY", "") if DOTENV_AVAILABLE else "",
        }
        
        # Initialize components
        self.setup_speech_recognition()
        self.setup_text_to_speech()
        
        # Load data
        self.schedule = self.load_schedule()
        self.contacts = self.load_contacts()
        self.reminders = []
        
        # Features
        self.commands = {
            "Greetings": ["hello", "hi", "hey", "good morning", "good afternoon"],
            "Time & Date": ["time", "clock", "date", "today"],
            "Schedule": ["schedule", "agenda", "appointments", "meetings"],
            "Weather": ["weather", "temperature", "forecast"],
            "Search": ["search", "google", "find"],
            "Calculator": ["calculate", "math", "multiply", "divide"],
            "System": ["system", "computer", "performance"],
            "Contacts": ["call", "contact", "phone"],
            "Media": ["play", "music", "pause", "stop"],
            "Exit": ["quit", "exit", "bye", "goodbye"]
        }
    
    def print_banner(self):
        """Display startup banner"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╭─────────────────────────────────────────────────────────────╮
│                                                             │
│     A R I A  -  Voice Assistant v{self.version}             │
│         Advanced Responsive Intelligence Assistant          │
│                                                             │
│     Welcome back, {Colors.BLUE}{self.user_name}{Colors.CYAN}!                              │
│     Session: {self.session_start_time.strftime('%H:%M:%S')} - {datetime.datetime.now().strftime('%Y-%m-%d')}                   │
│     Ready to assist with your daily tasks                   │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
{Colors.END}"""
        print(banner)
    
    def print_features(self):
        """Display available features"""
        print(f"{Colors.BOLD}{Colors.PURPLE}Available Commands:{Colors.END}")
        print(f"{Colors.DIM}{'─' * 60}{Colors.END}")
        
        for category, commands in self.commands.items():
            example = commands[0] if commands else "N/A"
            print(f"{Colors.CYAN}{category:<20}{Colors.WHITE} Try: '{example}'{Colors.END}")
        
        print(f"{Colors.DIM}{'─' * 60}{Colors.END}")
        print(f"{Colors.YELLOW}Tip: Speak naturally and clearly for best results{Colors.END}")
        print()
    
    def setup_speech_recognition(self):
        """Initialize speech recognition"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        print(f"{Colors.BLUE}Calibrating microphone...{Colors.END}")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Optimize settings
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        print(f"{Colors.GREEN}Microphone ready{Colors.END}")
    
    def setup_text_to_speech(self):
        """Initialize text-to-speech"""
        self.tts = pyttsx3.init()
        
        # Get available voices and try to set a pleasant one
        voices = self.tts.getProperty('voices')
        for voice in voices:
            if any(word in voice.name.lower() for word in ['zira', 'hazel', 'susan', 'female']):
                self.tts.setProperty('voice', voice.id)
                break
        
        # Set voice properties
        self.tts.setProperty('rate', self.config['voice_rate'])
        self.tts.setProperty('volume', self.config['voice_volume'])
        
        print(f"{Colors.GREEN}Voice engine ready{Colors.END}")
    
    def load_schedule(self) -> List[Dict]:
        """Load schedule data"""
        schedule_file = Path("schedule.json")
        default_schedule = [
            {
                "time": "10:00",
                "title": "Sales Meeting with Egi",
                "location": "Conference Room A",
                "priority": "high"
            },
            {
                "time": "17:00", 
                "title": "Coffee with Sophie",
                "location": "Starbucks Downtown",
                "priority": "medium"
            }
        ]
        
        if schedule_file.exists():
            try:
                with open(schedule_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Save default schedule
        with open(schedule_file, 'w') as f:
            json.dump(default_schedule, f, indent=2)
        
        return default_schedule
    
    def load_contacts(self) -> Dict:
        """Load contacts data"""
        contacts_file = Path("contacts.json")
        default_contacts = {
            "egi": {"name": "Egi", "phone": "+62-xxx-xxx-1234", "email": "egi@company.com"},
            "sophie": {"name": "Sophie", "phone": "+62-xxx-xxx-5678", "email": "sophie@example.com"}
        }
        
        if contacts_file.exists():
            try:
                with open(contacts_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        with open(contacts_file, 'w') as f:
            json.dump(default_contacts, f, indent=2)
        
        return default_contacts
    
    def speak(self, text: str, emotion: str = "neutral"):
        """Speak with visual feedback"""
        self.is_speaking = True
        
        # Emotion icons
        emotions = {
            "happy": "Happy", "excited": "Excited", "thinking": "Thinking", 
            "neutral": "Speaking", "concerned": "Concerned", "greeting": "Greeting"
        }
        
        icon = emotions.get(emotion, "Speaking")
        
        # Visual feedback
        print(f"{Colors.CYAN}{Colors.BOLD}[{icon}] {self.assistant_name}:{Colors.END} {Colors.WHITE}{text}{Colors.END}")
        
        # Speak the text
        self.tts.say(text)
        self.tts.runAndWait()
        
        self.is_speaking = False
        self.conversation_count += 1
    
    def listen(self) -> Optional[str]:
        """Listen for voice input"""
        if not SPEECH_RECOGNITION_AVAILABLE or sr is None:
            print(f"{Colors.RED}❌ Speech recognition not available{Colors.END}")
            return None
            
        self.is_listening = True
        
        try:
            print(f"{Colors.YELLOW}Listening... (speak now){Colors.END}")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=self.config['listen_timeout'])
            
            print(f"{Colors.BLUE}Processing...{Colors.END}")
            text = self.recognizer.recognize_google(audio)
            
            print(f"{Colors.GREEN}{Colors.BOLD}{self.user_name}:{Colors.END} {Colors.WHITE}{text}{Colors.END}")
            return text.lower()
            
        except Exception as e:
            # Handle all speech recognition exceptions generically
            if "WaitTimeoutError" in str(type(e)):
                print(f"{Colors.DIM}Listening timeout{Colors.END}")
            elif "UnknownValueError" in str(type(e)):
                print(f"{Colors.RED}Could not understand audio{Colors.END}")
            elif "RequestError" in str(type(e)):
                print(f"{Colors.RED}Speech recognition error: {e}{Colors.END}")
            else:
                print(f"{Colors.RED}Error: {e}{Colors.END}")
            return None
        finally:
            self.is_listening = False
    
    def get_weather(self, city: str = "Jakarta") -> str:
        """Get weather information"""
        if not REQUESTS_AVAILABLE:
            return "Weather service requires the requests library. Please install it with: pip install requests"
        
        if not self.config['weather_api_key']:
            return "I need a weather API key to provide weather information. You can get one free from OpenWeatherMap!"
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": self.config['weather_api_key'],
                "units": "metric"
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                
                return f"Weather in {city}: {description}, {temp}°C, humidity {humidity}%"
            else:
                return "Sorry, couldn't get weather information right now."
                
        except Exception:
            return "Weather service is currently unavailable."
    
    def calculate(self, expression: str) -> str:
        """Safe calculator"""
        try:
            # Clean the expression
            expression = expression.replace('calculate', '').replace('what is', '').strip()
            
            # Word replacements
            replacements = {
                'plus': '+', 'add': '+', 'and': '+',
                'minus': '-', 'subtract': '-',
                'times': '*', 'multiply': '*', 'multiplied by': '*',
                'divided by': '/', 'divide': '/',
                'squared': '**2'
            }
            
            for word, symbol in replacements.items():
                expression = expression.replace(word, symbol)
            
            # Safe evaluation
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"The answer is {result}"
            else:
                return "I can only do basic math calculations."
                
        except Exception:
            return "I couldn't understand that calculation. Please try again."
    
    def get_system_info(self) -> str:
        """Get system information"""
        try:
            import psutil
            
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return f"System status: CPU {cpu}%, Memory {memory.percent}%, Disk {(disk.used/disk.total)*100:.1f}%"
            
        except ImportError:
            return "System monitoring requires psutil. Install with: pip install psutil"
        except Exception as e:
            return f"Could not retrieve system information: {str(e)}"
    
    def process_command(self, command: str) -> tuple[str, str]:
        """Process voice commands intelligently"""
        
        # Greetings
        if any(word in command for word in self.commands["Greetings"]):
            hour = datetime.datetime.now().hour
            if hour < 12:
                greeting = "Good morning"
            elif hour < 17:
                greeting = "Good afternoon"
            else:
                greeting = "Good evening"
            
            return f"{greeting}, {self.user_name}! I'm {self.assistant_name}, your voice assistant. How can I help you today?", "greeting"
        
        # Time & Date
        elif any(word in command for word in self.commands["Time & Date"]):
            now = datetime.datetime.now()
            if 'time' in command or 'clock' in command:
                return f"The current time is {now.strftime('%I:%M %p')}", "neutral"
            else:
                return f"Today is {now.strftime('%A, %B %d, %Y')}", "neutral"
        
        # Schedule
        elif any(word in command for word in self.commands["Schedule"]):
            if self.schedule:
                schedule_text = "Your schedule for today: "
                for item in self.schedule:
                    schedule_text += f"{item['time']} - {item['title']} at {item['location']}. "
                return schedule_text, "neutral"
            else:
                return "You have no appointments scheduled for today.", "neutral"
        
        # Weather
        elif any(word in command for word in self.commands["Weather"]):
            city = "Jakarta"
            words = command.split()
            if 'in' in words:
                try:
                    city_index = words.index('in') + 1
                    if city_index < len(words):
                        city = words[city_index]
                except:
                    pass
            
            return self.get_weather(city), "neutral"
        
        # Search
        elif any(word in command for word in self.commands["Search"]):
            search_query = command.replace('search', '').replace('for', '').strip()
            if search_query:
                search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                webbrowser.open(search_url)
                return f"I've opened a web search for {search_query}", "happy"
            else:
                return "What would you like me to search for?", "neutral"
        
        # Calculator
        elif any(word in command for word in self.commands["Calculator"]):
            return self.calculate(command), "thinking"
        
        # System
        elif any(word in command for word in self.commands["System"]):
            return self.get_system_info(), "neutral"
        
        # Contacts
        elif any(word in command for word in self.commands["Contacts"]):
            for name, contact in self.contacts.items():
                if name.lower() in command:
                    return f"{contact['name']}'s contact: Phone {contact['phone']}, Email {contact['email']}", "neutral"
            return f"Available contacts: {', '.join([c['name'] for c in self.contacts.values()])}", "neutral"
        
        # Media
        elif any(word in command for word in self.commands["Media"]):
            return "Media control feature is coming soon! I'll be able to control your music player.", "excited"
        
        # Exit
        elif any(word in command for word in self.commands["Exit"]):
            return "goodbye", "happy"
        
        # Default
        else:
            return "I can help with time, weather, schedule, calculations, web search, and more. What would you like to do?", "thinking"
    
    def show_session_stats(self):
        """Show session statistics"""
        duration = datetime.datetime.now() - self.session_start_time
        print(f"\n{Colors.CYAN}{Colors.BOLD}Session Statistics:{Colors.END}")
        print(f"{Colors.WHITE}Duration: {duration}{Colors.END}")
        print(f"{Colors.WHITE}Conversations: {self.conversation_count}{Colors.END}")
        print(f"{Colors.WHITE}Commands available: {len(self.commands)}{Colors.END}")
    
    def run(self):
        """🚀 Main application loop"""
        try:
            # Clear screen and show banner
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
            self.print_features()
            
            # Initial greeting
            self.speak(
                f"Hello {self.user_name}! I'm {self.assistant_name}, your advanced voice assistant. "
                f"I'm ready to help you with various tasks. Just speak naturally!",
                "greeting"
            )
            
            # Main conversation loop
            while True:
                try:
                    command = self.listen()
                    
                    if command is None:
                        continue
                    
                    response, emotion = self.process_command(command)
                    
                    if response == "goodbye":
                        self.speak(f"Goodbye, {self.user_name}! Thank you for using {self.assistant_name}. Have a wonderful day!", "happy")
                        break
                    
                    self.speak(response, emotion)
                    time.sleep(0.5)
                    
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}Greeting Manual exit detected{Colors.END}")
                    self.speak("Goodbye! Exiting gracefully.", "happy")
                    break
                except Exception as e:
                    print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
                    self.speak("I encountered an error. Let me try again.", "concerned")
        
        except Exception as e:
            print(f"{Colors.RED}💥 Critical error: {e}{Colors.END}")
        
        finally:
            # Show session stats and cleanup
            self.show_session_stats()
            print(f"\n{Colors.CYAN}{Colors.BOLD}✨ Thank you for using {self.assistant_name}! ✨{Colors.END}")

def main():
    """🎯 Application entry point"""
    try:
        assistant = AriaAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Greeting Goodbye!{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}💥 Error starting assistant: {e}{Colors.END}")

if __name__ == "__main__":
    main()

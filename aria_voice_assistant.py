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
            "Greetings": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
            "Time & Date": ["time", "clock", "date", "today", "what time", "current time"],
            "Schedule": ["schedule", "agenda", "appointments", "meetings", "calendar"],
            "Weather": ["weather", "temperature", "forecast", "climate", "how hot", "how cold"],
            "Search": ["search", "google", "find", "look up", "look for", "browse"],
            "Calculator": ["calculate", "math", "multiply", "divide", "add", "subtract", "what is", "what's"],
            "System": ["system", "computer", "performance", "cpu", "memory", "battery"],
            "Contacts": ["call", "contact", "phone", "email", "reach"],
            "Media": ["play", "music", "pause", "stop", "song", "video"],
            "Exit": ["quit", "exit", "bye", "goodbye", "stop", "close"]
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
        
        # For demo purposes, provide mock weather data
        if not self.config['weather_api_key'] or self.config['weather_api_key'] == "demo_key":
            return f"Demo weather for {city}: Partly cloudy, 28°C, humidity 65%. Get your free API key from OpenWeatherMap for real weather data!"
        
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
            expression = expression.replace('calculate', '').replace('what is', '').replace('what\'s', '').strip()
            
            # Word replacements
            replacements = {
                'plus': '+', 'add': '+', 'and': '+',
                'minus': '-', 'subtract': '-', 'take away': '-',
                'times': '*', 'multiply': '*', 'multiplied by': '*', 'x': '*',
                'divided by': '/', 'divide': '/', 'over': '/',
                'squared': '**2', 'cubed': '**3',
                'to the power of': '**', 'power': '**'
            }
            
            for word, symbol in replacements.items():
                expression = expression.replace(word, symbol)
            
            # Handle common phrases
            if 'square root' in expression:
                num = expression.replace('square root of', '').strip()
                try:
                    result = float(num) ** 0.5
                    return f"The square root of {num} is {result:.2f}"
                except:
                    return "Please specify a number for square root calculation."
            
            # Clean up extra spaces
            expression = ' '.join(expression.split())
            
            # Safe evaluation - only allow basic math operations
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                # Replace common spoken numbers
                expression = expression.replace('zero', '0').replace('one', '1').replace('two', '2')
                expression = expression.replace('three', '3').replace('four', '4').replace('five', '5')
                expression = expression.replace('six', '6').replace('seven', '7').replace('eight', '8')
                expression = expression.replace('nine', '9').replace('ten', '10')
                
                result = eval(expression)
                return f"The answer is {result}"
            else:
                return "I can only do basic math calculations with numbers and operators."
                
        except ZeroDivisionError:
            return "Cannot divide by zero!"
        except Exception:
            return "I couldn't understand that calculation. Try saying something like 'calculate 5 plus 3' or 'what is 10 times 2'."
    
    def get_system_info(self) -> str:
        """Get system information"""
        try:
            import psutil
            import platform
            
            # Get system info
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            battery = None
            
            try:
                battery = psutil.sensors_battery()
            except:
                pass
            
            # Format response
            response = f"System status: CPU usage {cpu_percent}%, Memory usage {memory.percent}%"
            
            if battery:
                battery_status = "charging" if battery.power_plugged else "on battery"
                response += f", Battery {battery.percent}% ({battery_status})"
            
            # Add OS info
            os_info = platform.system()
            response += f". Running on {os_info}"
            
            return response
            
        except ImportError:
            # Fallback system info without psutil
            import platform
            return f"Basic system info: Running on {platform.system()} {platform.release()}. For detailed monitoring, install psutil with: pip install psutil"
        except Exception as e:
            return f"Could not retrieve complete system information. {str(e)}"
    
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
            # Extract search query
            search_query = command
            for word in ['search', 'for', 'google', 'find', 'look up', 'look for']:
                search_query = search_query.replace(word, '', 1).strip()
            
            if search_query:
                search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                try:
                    webbrowser.open(search_url)
                    return f"I've opened a web search for '{search_query}' in your browser", "happy"
                except Exception:
                    return f"I would search for '{search_query}' but couldn't open your browser. Try opening Google manually.", "concerned"
            else:
                return "What would you like me to search for? Try saying 'search for Python programming'", "neutral"
        
        # Calculator
        elif any(word in command for word in self.commands["Calculator"]):
            return self.calculate(command), "thinking"
        
        # System
        elif any(word in command for word in self.commands["System"]):
            return self.get_system_info(), "neutral"
        
        # Contacts
        elif any(word in command for word in self.commands["Contacts"]):
            # Check if user mentioned a specific contact
            contact_found = False
            for name, contact in self.contacts.items():
                if name.lower() in command or contact['name'].lower() in command:
                    contact_found = True
                    if 'call' in command or 'phone' in command:
                        return f"I would call {contact['name']} at {contact['phone']}, but I can't make actual calls yet. You can call them manually!", "neutral"
                    else:
                        return f"{contact['name']}'s contact information: Phone {contact['phone']}, Email {contact['email']}", "neutral"
            
            if not contact_found:
                contact_names = [c['name'] for c in self.contacts.values()]
                return f"I have contacts for: {', '.join(contact_names)}. Try saying 'call [name]' or 'contact [name]'", "neutral"
        
        # Media
        elif any(word in command for word in self.commands["Media"]):
            if 'play' in command:
                # Extract song/artist name
                music_query = command.replace('play', '').strip()
                if music_query:
                    # Open YouTube search for the song
                    youtube_url = f"https://www.youtube.com/results?search_query={music_query.replace(' ', '+')}"
                    try:
                        webbrowser.open(youtube_url)
                        return f"I've opened YouTube search for '{music_query}'. Click on a video to play it!", "excited"
                    except:
                        return f"I would play '{music_query}' but couldn't open your browser. Try opening YouTube manually.", "concerned"
                else:
                    return "What would you like me to play? Try saying 'play some jazz music' or 'play Taylor Swift'", "neutral"
            elif 'pause' in command or 'stop' in command:
                return "I can't control media playback directly yet, but you can use your keyboard spacebar to pause/play most media players!", "neutral"
            else:
                return "I can help you find music on YouTube! Try saying 'play [song name]' or 'play [artist name]'", "excited"
        
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

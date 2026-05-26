import subprocess
import requests
import urllib.parse
import json

def speak(text):
    print(f"\n[JANO_AI]: {text}")
    subprocess.run(["termux-tts-speak", text])

def listen():
    print("\n[JANO_AI is listening...]")
    try:
        process = subprocess.Popen(["termux-speech-to-text"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        user_text = stdout.strip()
        if user_text and "ERROR" not in user_text:
            print(f"[You]: {user_text}")
            return user_text
        return None
    except Exception:
        return None

def ask_ai(question):
    # ጥያቄን ወደ AI መላክ (ለአጭር መልስ መመሪያ ተሰጥቶታል)
    prompt = f"You are JANO_AI. Give short answers. Question: {question}"
    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else "I am offline right now."
    except Exception:
        return "Network connection failed."

if __name__ == "__main__":
    speak("System fully operational. I am JANO_AI. created by Yoseph Alganeh. How can I assist you today?")
    
    while True:
        cmd_raw = listen()
        
        # ድምፅ ካልሰማ ወዲያውኑ ወደ ማዳመጥ (listen) ይመለሳል
        if not cmd_raw:
            continue
            
        cmd = cmd_raw.lower()

        # --------------------------------------------------------
        # 1. ማቆሚያ ትዕዛዝ (Stop Command)
        # --------------------------------------------------------
        if "stop" in cmd or "exit" in cmd or "shut down" in cmd:
            speak("Shutting down all systems. Goodbye sir!")
            break

        # --------------------------------------------------------
        # 2. የ Termux API ትዕዛዞች (System Controls)
        # --------------------------------------------------------
        
        # የባትሪ ሁኔታ
        elif "battery" in cmd:
            try:
                result = subprocess.check_output(["termux-battery-status"], text=True)
                data = json.loads(result)
                speak(f"Your battery is at {data['percentage']} percent.")
            except Exception:
                speak("I couldn't read the battery status.")
                
        # የባትሪ መብራት ማብራት
        elif "torch on" in cmd or "flashlight on" in cmd:
            subprocess.run(["termux-torch", "on"])
            speak("Flashlight activated.")
            
        # የባትሪ መብራት ማጥፋት
        elif "torch off" in cmd or "flashlight off" in cmd:
            subprocess.run(["termux-torch", "off"])
            speak("Flashlight deactivated.")

        # ክሊፕቦርድ ማንበብ (Copy የተደረገ ጽሑፍ)
        elif "read clipboard" in cmd or "clipboard" in cmd:
            try:
                text = subprocess.check_output(["termux-clipboard-get"], text=True)
                if text.strip():
                    speak(f"Your clipboard says: {text}")
                else:
                    speak("Your clipboard is empty.")
            except Exception:
                speak("Could not access clipboard.")

        # ዋይፋይ (WiFi) ማብራት
        elif "wifi on" in cmd or "turn on wifi" in cmd:
            subprocess.run(["termux-wifi-enable", "true"])
            speak("Wi-Fi has been turned on.")

        # ዋይፋይ (WiFi) ማጥፋት
        elif "wifi off" in cmd or "turn off wifi" in cmd:
            subprocess.run(["termux-wifi-enable", "false"])
            speak("Wi-Fi has been turned off.")

        # ፎቶ ማንሳት (የስልኩን ካሜራ በመጠቀም)
        elif "take a photo" in cmd or "take a picture" in cmd:
            speak("Taking a photo now.")
            # ፎቶውን 'photo.jpg' በሚል ስም ያስቀምጠዋል
            subprocess.run(["termux-camera-photo", "photo.jpg"])
            speak("Photo captured and saved successfully.")

        # ያለህበትን ቦታ (Location) ማወቅ
        elif "location" in cmd or "where am i" in cmd:
            speak("Fetching GPS coordinates. Please wait.")
            try:
                loc = subprocess.check_output(["termux-location"], text=True)
                loc_data = json.loads(loc)
                speak(f"Your latitude is {loc_data['latitude']} and longitude is {loc_data['longitude']}")
            except Exception:
                speak("I could not get the GPS location. Make sure location services are on.")

        # --------------------------------------------------------
        # 3. AI ን መጠየቅ (General AI Query)
        # --------------------------------------------------------
        else:
            # ሌላ ማንኛውም ጥያቄ ከሆነ (ምንም ትዕዛዝ ካልሆነ) ወደ AI ሰርቨር ይላካል
            ai_answer = ask_ai(cmd_raw)
            speak(ai_answer)

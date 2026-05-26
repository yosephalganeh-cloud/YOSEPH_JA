import os
import json
import subprocess
import requests
import urllib.parse
import time

CONFIG_FILE = "jano_config.json"

def speak(text, mode):
    """Outputs the response via terminal print and conditionally via TTS if in voice mode."""
    print(f"\n[JANO_AI]: {text}")
    if mode == "voice":
        subprocess.run(["termux-tts-speak", text])

def get_input(mode):
    """Captures user input either from voice recognition or direct terminal typing."""
    if mode == "voice":
        try:
            process = subprocess.Popen(["termux-speech-to-text"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, _ = process.communicate()
            user_text = stdout.strip()
            if user_text and "ERROR" not in user_text:
                print(f"[You (Voice)]: {user_text}")
                return user_text
            return None
        except:
            return None
    else:
        try:
            user_text = input("\n[You (Type)]: ").strip()
            return user_text if user_text else None
        except (KeyboardInterrupt, EOFError):
            return "stop"

def ask_ai(question, gender):
    """Sends the prompt to the AI server using a multi-model fallback to prevent 429/overloading errors."""
    prompt = (
        f"You are JANO_AI, a smart voice assistant developed by Yoseph Alganeh. The user's gender is {gender}. "
        f"CRITICAL RULE: Respond strictly and purely in English. Keep answers extremely fast, short, direct, and clean. Do not use bold markdown asterisks. Question: {question}"
    )
    
    # Fast multi-model lane to bypass Pollinations 429 congestion completely
    models = ["mistral", "llama", "openai"]
    
    for model in models:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?model={model}&cache=false"
        try:
            response = requests.get(url, timeout=12)
            if response.status_code == 200 and response.text.strip():
                # Clean up markdown bold asterisks for terminal aesthetic
                return response.text.strip().replace("**", "").replace("*", "")
        except:
            continue
            
    return "All AI inference lanes are packed. Please try resending in a few seconds."

def get_battery_info():
    try:
        output = subprocess.check_output(["termux-battery-status"], text=True)
        data = json.loads(output)
        return f"Battery is at {data['percentage']}%, and status is {data['status']}."
    except:
        return "Unable to fetch battery information."

def get_wifi_info():
    try:
        output = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        data = json.loads(output)
        if data.get("supplicant_state") == "COMPLETED":
            return f"Connected to Wi-Fi network: {data.get('ssid', 'unknown')}."
        return "Wi-Fi is currently disconnected."
    except:
        return "Unable to fetch Wi-Fi information."

def load_or_create_config():
    """Loads saved profile configuration or triggers a first-time setup without language prompts."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config["gender"]
        except:
            pass
            
    print("\n--- JANO_AI FIRST TIME SETUP ---")
    
    # Ask Gender (Supports m/f/male/female)
    while True:
        g_input = input("Select Gender - Male or Female (m/f): ").strip().lower()
        if g_input in ['m', 'male', 'ወንድ']:
            gender = "Male"
            break
        elif g_input in ['f', 'female', 'ሴት']:
            gender = "Female"
            break
        print("Invalid choice. Please enter 'm' or 'f'.")

    # Save to local file (Language defaults strictly to English now)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"gender": gender, "language": "English"}, f)
        
    print("Profile configuration saved successfully!\n")
    return gender

if __name__ == "__main__":
    # Load the remembered profile configuration
    gender = load_or_create_config()
    
    # Ask input mode every single time the script starts
    print("--- CHOOSE INPUT MODE ---")
    while True:
        mode_input = input("Use Typing or Voice mode? (t/v): ").strip().lower()
        if mode_input in ['t', 'typing']:
            input_mode = "typing"
            break
        elif mode_input in ['v', 'voice']:
            input_mode = "voice"
            break
        print("Invalid input. Type 't' for Typing or 'v' for Voice.")

    speak(f"System online. Profile loaded as {gender}. How can I assist you today?", input_mode)
    
    # Core operational loop - zero unnecessary delays
    while True:
        user_speech = get_input(input_mode)
        if not user_speech:
            continue
            
        cmd = user_speech.lower()

        # ==========================================
        # TERMUX API UTILITIES
        # ==========================================
        if "battery" in cmd or "ባትሪ" in cmd:
            speak(get_battery_info(), input_mode)
            
        elif "wifi" in cmd or "ዋይፋይ" in cmd:
            speak(get_wifi_info(), input_mode)
        
        elif "torch on" in cmd or "flashlight on" in cmd or "መብራት አብራ" in cmd:
            subprocess.run(["termux-torch", "on"])
            speak("Flashlight activated.", input_mode)
            
        elif "torch off" in cmd or "flashlight off" in cmd or "መብራት አጥፋ" in cmd:
            subprocess.run(["termux-torch", "off"])
            speak("Flashlight deactivated.", input_mode)

        elif "clipboard" in cmd:
            try:
                text = subprocess.check_output(["termux-clipboard-get"], text=True)
                speak(f"Clipboard details: {text}", input_mode)
            except:
                speak("Clipboard workspace is empty.", input_mode)
                
        elif "vibrate" in cmd or "ንዘር" in cmd:
            speak("Device vibrating.", input_mode)
            subprocess.run(["termux-vibrate", "-d", "1000"])

        elif "stop" in cmd or "exit" in cmd or "አቁም" in cmd:
            speak("Deactivating system. Goodbye.", input_mode)
            break

        # ==========================================
        # FAST DEPLOYMENT TO ARTIFICIAL INTELLIGENCE
        # ==========================================
        else:
            ai_reply = ask_ai(user_speech, gender)
            speak(ai_reply, input_mode)
        
        # Prevent microphone overlapping loop recursively only on voice mode
        if input_mode == "voice":
            time.sleep(1)

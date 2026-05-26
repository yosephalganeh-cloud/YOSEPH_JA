import subprocess
import requests
import time
import urllib.parse
import json
import os

CONFIG_FILE = "jano_config.json"

def speak(text, interaction_mode):
    """Outputs text to the console and speaks it aloud if voice mode is active."""
    print(f"\n[JANO_AI]: {text}")
    if interaction_mode == "voice":
        subprocess.run(["termux-tts-speak", text])

def listen(interaction_mode):
    """Gets input from the user via microphone or keyboard typing."""
    if interaction_mode == "voice":
        print("\n[JANO_AI is listening...] (Speak now)")
        try:
            process = subprocess.Popen(["termux-speech-to-text"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            user_text = stdout.strip()
            if user_text and "ERROR" not in user_text:
                print(f"[You]: {user_text}")
                return user_text
            return None
        except:
            return None
    else:
        user_text = input("\n[You - Type here]: ").strip()
        return user_text if user_text else None

def ask_ai(question, gender, language):
    """Sends the user prompt to the AI server enforcing custom identity, gender, and language."""
    prompt = (
        f"You are JANO_AI, a highly intelligent voice assistant. The user is {gender}. "
        f"The user's preferred language is {language}. CRITICAL RULE: If the user speaks/writes "
        f"in Amharic, you MUST reply in Amharic. If the user speaks/writes in English, you MUST reply "
        f"in English. Keep your responses short, natural, and highly accurate. User says: {question}"
    )
    
    safe_prompt = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{safe_prompt}"
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else "Sorry, my network brain is currently offline."
    except:
        return "Network connection failed."

def get_battery_info():
    """Fetches real-time device battery percentage and charging status."""
    try:
        output = subprocess.check_output(["termux-battery-status"], text=True)
        data = json.loads(output)
        return f"Your battery is at {data['percentage']} percent, and the status is {data['status']}."
    except:
        return "I am unable to read the battery status right now."

def get_wifi_info():
    """Fetches device Wi-Fi connectivity parameters."""
    try:
        output = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        data = json.loads(output)
        if data.get("supplicant_state") == "COMPLETED":
            return f"You are connected to Wi-Fi. The network name is {data.get('ssid', 'unknown')}."
        return "You are currently not connected to any Wi-Fi network."
    except:
        return "I am unable to retrieve Wi-Fi data."

def load_user_config():
    """Loads stored user settings if they exist."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def save_user_config(gender, language):
    """Saves user configurations persistently to a local JSON file."""
    config = {"gender": gender, "language": language}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def setup_user(interaction_mode):
    """Handles first-time profile creation or loads an existing one."""
    config = load_user_config()
    if config:
        return config["gender"], config["language"]
    
    # 1. Select Gender
    speak("System initialization. Please specify your gender. Say or type Male or Female.", interaction_mode)
    user_gender = "Unknown"
    while True:
        ans = listen(interaction_mode)
        if ans:
            ans_lower = ans.lower()
            if "female" in ans_lower or "ሴት" in ans_lower:
                user_gender = "Female"
                break
            elif "male" in ans_lower or "ወንድ" in ans_lower:
                user_gender = "Male"
                break
            else:
                speak("Selection unrecognized. Please state Male or Female.", interaction_mode)
    
    # 2. Select Language
    speak("Profile updated. Now, choose your preferred language. Say or type English or Amharic.", interaction_mode)
    user_lang = "English"
    while True:
        ans = listen(interaction_mode)
        if ans:
            ans_lower = ans.lower()
            if "amharic" in ans_lower or "አማርኛ" in ans_lower:
                user_lang = "Amharic"
                break
            elif "english" in ans_lower or "እንግሊዝኛ" in ans_lower:
                user_lang = "English"
                break
            else:
                speak("Selection unrecognized. Please state English or Amharic.", interaction_mode)
                
    save_user_config(user_gender, user_lang)
    speak(f"Configuration profile successfully created. Welcome aboard.", interaction_mode)
    return user_gender, user_lang

if __name__ == "__main__":
    # Always prompt for interaction mode at boot
    print("\n==============================")
    print("      JANO_AI INITIALIZATION  ")
    print("==============================")
    print("Choose interaction mode:")
    print("1. voice")
    print("2. typing")
    
    mode = input("Enter mode choice (voice/typing): ").strip().lower()
    while mode not in ["voice", "typing"]:
        mode = input("Invalid option. Please type 'voice' or 'typing': ").strip().lower()
        
    # Run user configuration profiles
    gender, language = setup_user(mode)
    speak(f"JANO_AI Engine Active. Mode set to {mode}. How can I assist you today?", mode)
    
    # Continuous core execution loop
    while True:
        cmd_raw = listen(mode)
        if not cmd_raw: 
            continue
            
        cmd = cmd_raw.lower()

        # ==========================================
        # TERMUX API UTILITIES & CONTROLS
        # ==========================================
        if "battery" in cmd or "ባትሪ" in cmd:
            speak(get_battery_info(), mode)
            
        elif "wifi" in cmd or "ዋይፋይ" in cmd:
            speak(get_wifi_info(), mode)
        
        elif "torch on" in cmd or "flashlight on" in cmd or "መብራት አብራ" in cmd:
            subprocess.run(["termux-torch", "on"])
            speak("Flashlight turned on.", mode)
            
        elif "torch off" in cmd or "flashlight off" in cmd or "መብራት አጥፋ" in cmd:
            subprocess.run(["termux-torch", "off"])
            speak("Flashlight turned off.", mode)

        elif "clipboard" in cmd:
            try:
                text = subprocess.check_output(["termux-clipboard-get"], text=True)
                speak(f"Current clipboard content is: {text}", mode)
            except:
                speak("Your system clipboard is empty.", mode)
                
        elif "vibrate" in cmd or "ንዘር" in cmd:
            speak("Activating device vibration.", mode)
            subprocess.run(["termux-vibrate", "-d", "1000"])

        elif "stop" in cmd or "exit" in cmd or "አቁም" in cmd:
            speak("Deactivating system modules. JANO_AI shutting down. Goodbye!", mode)
            break

        # ==========================================
        # CORE AI ASSISTANT PROCESSING
        # ==========================================
        else:
            ai_reply = ask_ai(cmd_raw, gender, language)
            speak(ai_reply, mode)
        
        time.sleep(0.5)

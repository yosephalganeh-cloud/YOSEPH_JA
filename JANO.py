import subprocess
import requests
import time
import urllib.parse
import json

def speak(text):
    print(f"\n[JANO_AI]: {text}")
    subprocess.run(["termux-tts-speak", text])

def listen():
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

def ask_ai(question, gender, language):
    # AI Prompt that strictly enforces bilingual and customized responses
    prompt = f"You are JANO_AI, a highly intelligent voice assistant. The user is {gender}. The user's preferred language is {language}. CRITICAL RULE: If the user asks in Amharic, you MUST reply in Amharic. If the user asks in English, you MUST reply in English. Keep your responses short, natural, and highly accurate. User says: {question}"
    
    safe_prompt = urllib.parse.quote(prompt)
    url = f"https://text.pollinations.ai/{safe_prompt}"
    try:
        response = requests.get(url)
        return response.text if response.status_code == 200 else "Sorry, my network brain is currently offline."
    except:
        return "Network connection failed."

def get_battery_info():
    try:
        output = subprocess.check_output(["termux-battery-status"], text=True)
        data = json.loads(output)
        return f"Your battery is at {data['percentage']} percent, and it is {data['status']}."
    except:
        return "I couldn't read the battery status."

def get_wifi_info():
    try:
        output = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        data = json.loads(output)
        if data.get("supplicant_state") == "COMPLETED":
            return f"You are connected to Wi-Fi. The network name is {data.get('ssid', 'unknown')}."
        return "You are not connected to Wi-Fi."
    except:
        return "I couldn't get the Wi-Fi information."

def setup_user():
    # 1. Ask Gender
    speak("System starting. Please tell me your gender. Say Male or Female.")
    user_gender = "Unknown"
    while True:
        ans = listen()
        if ans:
            ans_lower = ans.lower()
            if "female" in ans_lower or "ሴት" in ans_lower:
                user_gender = "Female"
                break
            elif "male" in ans_lower or "ወንድ" in ans_lower:
                user_gender = "Male"
                break
            else:
                speak("I didn't catch that. Please say Male or Female.")
    
    # 2. Ask Language
    speak("Thank you. Now, which language do you prefer? Say English or Amharic.")
    user_lang = "English"
    while True:
        ans = listen()
        if ans:
            ans_lower = ans.lower()
            if "amharic" in ans_lower or "አማርኛ" in ans_lower:
                user_lang = "Amharic"
                break
            elif "english" in ans_lower or "እንግሊዝኛ" in ans_lower:
                user_lang = "English"
                break
            else:
                speak("Please say English or Amharic.")
                
    speak(f"Setup complete. Welcome to JANO AI. Created by Yoseph Alganeh. I am ready.")
    return user_gender, user_lang

if __name__ == "__main__":
    # Run the setup first
    gender, language = setup_user()
    
    # Infinite loop for continuous listening without saying "continue"
    while True:
        cmd_raw = listen()
        
        # If nothing heard, just loop back and open mic again silently
        if not cmd_raw: 
            continue
            
        cmd = cmd_raw.lower()

        # ==========================================
        # TERMUX API SYSTEM CONTROLS
        # ==========================================
        if "battery" in cmd or "ባትሪ" in cmd:
            speak(get_battery_info())
            
        elif "wifi" in cmd or "ዋይፋይ" in cmd:
            speak(get_wifi_info())
        
        elif "torch on" in cmd or "flashlight on" in cmd or "መብራት አብራ" in cmd:
            subprocess.run(["termux-torch", "on"])
            speak("Flashlight turned on.")
            
        elif "torch off" in cmd or "flashlight off" in cmd or "መብራት አጥፋ" in cmd:
            subprocess.run(["termux-torch", "off"])
            speak("Flashlight turned off.")

        elif "clipboard" in cmd:
            try:
                text = subprocess.check_output(["termux-clipboard-get"], text=True)
                speak(f"Clipboard content is: {text}")
            except:
                speak("Clipboard is empty.")
                
        elif "vibrate" in cmd or "ንዘር" in cmd:
            speak("Vibrating now.")
            subprocess.run(["termux-vibrate", "-d", "1000"])

        elif "stop" in cmd or "exit" in cmd or "አቁም" in cmd:
            speak("Shutting down JANO AI. Have a great day!")
            break

        # ==========================================
        # ASK AI (If it's not a system command)
        # ==========================================
        else:
            ai_reply = ask_ai(cmd_raw, gender, language)
            speak(ai_reply)
        
        # A brief pause before the mic reopens
        time.sleep(1)

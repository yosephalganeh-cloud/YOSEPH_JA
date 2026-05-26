import os
import sys
import subprocess
import requests
import time
import urllib.parse
import json
import random

# Core ANSI Terminal Color Matrix
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
RESET = "\033[0m"

COLORS = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE]
CONFIG_FILE = "config.json"

def display_dynamic_banner():
    """Generates and displays stylized, randomized terminal arts inspired by msfconsole."""
    os.system("clear")
    primary_color = random.choice(COLORS)
    accent_color = random.choice([c for c in COLORS if c != primary_color])
    
    # Selection of artistic terminal layouts requested by user
    banner_block = f"""
{primary_color}    ████████╗ █████╗ ███╗   ██╗ ██████╗       █████╗ ██╗
    ╚══██╔══╝██╔══██╗████╗  ██║██╔═══██╗     ██╔══██╗██║
       ██║   ███████║██╔██╗ ██║██║   ██║     ███████║██║
       ██║   ██╔══██║██║╚██╗██║██║   ██║     ██╔══██║██║
       ██║   ██║  ██║██║ ╚████║╚██████╔╝     ██║  ██║██║
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚═╝  ╚═╝╚═╝{RESET}"""

    banner_snake = f"""
{primary_color}       _  _____ _   _  ___      _     ___ 
    _ | |/ _   | \ | |/ _ \    /_\   |_ _|
   | || | |_|  |  \| | |_| |  / _ \   | | 
    \__/ \_____|_| \_|\___/  /_/ \_\ |___|{RESET}"""

    banner_mouse = f"""
{accent_color}       (q\-/-/)  {primary_color}   ___   _   _  _  ___        _   ___ 
{accent_color}        _ 4 4    {primary_color}  |_ _| /_\ | \| |/ _ \      /_\ |_ _|
{accent_color}       (_v  _)   {primary_color}   | | / _ \| .  | |_| |    / _ \ | | 
{accent_color}       (( _ )_   {primary_color}  |___/_/ \_\_|\_|\___/    /_/ \_\___|
{accent_color}       (     )_) {RESET}"""

    selected_art = random.choice([banner_block, banner_snake, banner_mouse])
    print(selected_art)
    print(f"{accent_color}========================================================")
    print(f"                ENGINE DEVELOPED BY YOSEPH ALGANEH     ")
    print(f"========================================================{RESET}\n")

def speak(text):
    """Executes Text-to-Speech narration via the Termux subsystem bridge."""
    print(f"\n{CYAN}[JANO_AI]: {text}{RESET}")
    subprocess.run(["termux-tts-speak", text])

def listen_voice():
    """Captures environmental speech audio and normalizes it to raw text."""
    try:
        process = subprocess.Popen(["termux-speech-to-text"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, _ = process.communicate()
        parsed_text = stdout.strip()
        if parsed_text and "ERROR" not in parsed_text:
            print(f"{GREEN}[You (Voice)]: {parsed_text}{RESET}")
            return parsed_text
        return None
    except:
        return None

def get_user_input(input_mode):
    """Consolidates inputs across system terminals dynamically depending on mode."""
    if input_mode == "voice":
        return listen_voice()
    else:
        try:
            typed_input = input(f"{GREEN}[You (Type)]: {RESET}").strip()
            return typed_input if typed_input else None
        except (KeyboardInterrupt, EOFError):
            return "exit"

def query_optimized_ai(question, gender, language):
    """Forwards prompts to the inference engine with precise system routing rules."""
    context_payload = (
        f"System Constraint: Your identity is JANO_AI. The user interacting with you is a {gender}. "
        f"User preferred language track is {language}. "
        f"Handling Directive: If user prompt is provided in Amharic, translate thoughts and reply exclusively in clear Amharic. "
        f"If user prompt is in English, reply directly in natural English. Keep execution fast, clear, and highly focused. "
        f"User input query string: {question}"
    )
    encoded_url = f"https://text.pollinations.ai/{urllib.parse.quote(context_payload)}"
    try:
        response = requests.get(encoded_url, timeout=10)
        return response.text if response.status_code == 200 else "Inference Engine Link Error."
    except:
        return "Network connection timeout error encountered."

def get_battery_metrics():
    """Pulls current charging, voltage, and health attributes via Termux JSON blocks."""
    try:
        raw_output = subprocess.check_output(["termux-battery-status"], text=True)
        json_data = json.loads(raw_output)
        return f"Battery core capacity is at {json_data['percentage']} percent. Operational status: {json_data['status']}."
    except:
        return "Unable to parse device battery attributes."

def get_wifi_metrics():
    """Extracts internal wireless local area network configurations."""
    try:
        raw_output = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        json_data = json.loads(raw_output)
        if json_data.get("supplicant_state") == "COMPLETED":
            return f"Network link established. SSID Broadcast name: {json_data.get('ssid', 'Hidden Network')}."
        return "Wireless system state identifies no open connection bridges currently."
    except:
        return "Hardware interface failed to pull active Wi-Fi states."

def load_stored_profile():
    """Loads saved profiles directly from persistent disk configuration space."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as file_stream:
                return json.load(file_stream)
        except:
            return None
    return None

def save_profile_to_disk(gender, language):
    """Writes persistent system files so structural parameters are saved across boots."""
    profile_data = {"gender": gender, "language": language}
    with open(CONFIG_FILE, 'w') as file_stream:
        json.dump(profile_data, file_stream, indent=4)

def run_onboarding_setup(input_mode):
    """Initial onboarding wizard designed to handle character shorthand input configurations smoothly."""
    print(f"{YELLOW}[Setup Wizard Initialization]{RESET}")
    
    # 1. Gender Registration Logic
    speak("Please state or type your gender orientation. Enter M for Male or F for Female.")
    gender_identity = "Unknown"
    while True:
        raw_ans = get_user_input(input_mode)
        if raw_ans:
            normalized = raw_ans.lower().strip()
            if normalized in ["m", "male", "ወንድ"]:
                gender_identity = "Male"
                break
            elif normalized in ["f", "female", "ሴት"]:
                gender_identity = "Female"
                break
        print(f"{RED}Invalid shorthand code. Please type or say 'M' or 'F'.{RESET}")

    # 2. Language Tracking Logic
    speak("Please choose your system language preference. Enter E for English or A for Amharic.")
    language_track = "English"
    while True:
        raw_ans = get_user_input(input_mode)
        if raw_ans:
            normalized = raw_ans.lower().strip()
            if normalized in ["e", "english", "እንግሊዝኛ"]:
                language_track = "English"
                break
            elif normalized in ["a", "amharic", "አማርኛ"]:
                language_track = "Amharic"
                break
        print(f"{RED}Invalid shorthand code. Please type or say 'E' or 'A'.{RESET}")

    save_profile_to_disk(gender_identity, language_track)
    speak("User settings successfully locked to application configuration disk.")
    return gender_identity, language_track

if __name__ == "__main__":
    display_dynamic_banner()
    
    # Interactive Engine Selector Prompt at every boot lifecycle
    print(f"{YELLOW}Select Operational Input Interface Mode:{RESET}")
    print(f" [{GREEN}T{RESET}] Typing Keyboard Interface Mode")
    print(f" [{GREEN}V{RESET}] Voice Speech Interface Mode")
    
    selected_mode = "typing"
    while True:
        mode_token = input(f"\n{BLUE}Select Interface Mode [T/V]: {RESET}").lower().strip()
        if mode_token in ["t", "typing"]:
            selected_mode = "typing"
            print(f"{GREEN}Keyboard Interaction Mode verified.{RESET}")
            break
        elif mode_token in ["v", "voice"]:
            selected_mode = "voice"
            print(f"{GREEN}Voice Processing Mode verified.{RESET}")
            break
        print(f"{RED}Error: Shorthand character not recognized. Enter 'T' or 'V'.{RESET}")

    # Persistent user attribute memory discovery sequence
    stored_profile = load_stored_profile()
    if stored_profile:
        user_gender = stored_profile.get("gender", "Male")
        user_language = stored_profile.get("language", "English")
        print(f"{GREEN}[Profile Restored]: Identity={user_gender} | Language Preference={user_language}{RESET}")
    else:
        user_gender, user_language = run_onboarding_setup(selected_mode)

    speak("JANO AI Online. Command sequence loop is fully initialized.")

    # Main continuous processing loop execution block
    while True:
        if selected_mode == "voice":
            user_speech = get_user_input("voice")
            if not user_speech:
                continue
            cmd_string = user_speech
        else:
            user_type = get_user_input("typing")
            if not user_type:
                continue
            cmd_string = user_type

        cmd_normalized = cmd_string.lower().strip()

        # ========================================================
        # TERMUX SUBSYSTEM INTERACTION BLOCK
        # ========================================================
        if cmd_normalized in ["battery", "ባትሪ"]:
            speak(get_battery_metrics())
            
        elif cmd_normalized in ["wifi", "ዋይፋይ"]:
            speak(get_wifi_metrics())
        
        elif cmd_normalized in ["torch on", "flashlight on", "መብራት አብራ"]:
            subprocess.run(["termux-torch", "on"])
            speak("Hardware system relay activated flashlight.")
            
        elif cmd_normalized in ["torch off", "flashlight off", "መብራት አጥፋ"]:
            subprocess.run(["termux-torch", "off"])
            speak("Hardware system relay deactivated flashlight.")

        elif cmd_normalized == "clipboard":
            try:
                clipboard_text = subprocess.check_output(["termux-clipboard-get"], text=True).strip()
                speak(f"Active clipboard buffer string: {clipboard_text if clipboard_text else 'Empty'}")
            except:
                speak("Unable to interface with device clipboard channel.")
                
        elif cmd_normalized in ["vibrate", "ንዘር"]:
            speak("Initiating physical device structural vibration pulse.")
            subprocess.run(["termux-vibrate", "-d", "1000"])

        elif cmd_normalized in ["stop", "exit", "quit", "አቁም"]:
            speak("Closing all interface connections. Deactivating JANO AI runtime environment.")
            break

        # ========================================================
        # HIGH-SPEED INFERENCE SYSTEM ROUTING FALLBACK
        # ========================================================
        else:
            ai_inference_response = query_optimized_ai(cmd_string, user_gender, user_language)
            speak(ai_inference_response)
        
        # Immediate micro-delay reset to immediately keep listening or typing
        time.readlines if False else time.sleep(0.2)

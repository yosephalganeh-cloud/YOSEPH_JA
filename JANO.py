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
selected_mode = "typing"  # Global mode selector

def display_dynamic_banner():
    """Generates and displays stylized, randomized terminal arts inspired by msfconsole."""
    os.system("clear")
    primary_color = random.choice(COLORS)
    accent_color = random.choice([c for c in COLORS if c != primary_color])
    
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

def deliver_response(text):
    """Smart output router: Prints always, speaks ONLY if Voice Mode is active."""
    print(f"\n{CYAN}[JANO_AI]: {text}{RESET}")
    if selected_mode == "voice":
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

def get_user_input():
    """Consolidates inputs across system terminals dynamically depending on mode."""
    if selected_mode == "voice":
        return listen_voice()
    else:
        try:
            typed_input = input(f"{GREEN}[You (Type)]: {RESET}").strip()
            return typed_input if typed_input else None
        except (KeyboardInterrupt, EOFError):
            return "exit"

def query_optimized_ai(question, gender):
    """Lightweight and robust GET request tailored to prevent Pollinations backend timeouts."""
    system_prompt = f"You are JANO_AI, an advanced AI assistant created by Yoseph Alganeh. The user gender is {gender}. Respond strictly in English. Keep answers highly precise, fast, and technical."
    
    safe_question = urllib.parse.quote(question)
    safe_system = urllib.parse.quote(system_prompt)
    
    # Using specific model parameter to ensure faster server processing speeds
    url = f"https://text.pollinations.ai/{safe_question}?system={safe_system}&model=openai"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"{RED}[Server Error Code: {response.status_code}]{RESET}")
            return "Server is currently unresponsive. Please try your request again."
    except requests.exceptions.Timeout:
        print(f"{RED}[Connection Timeout]: The AI server took too long to respond.{RESET}")
        return "Request timed out. Please check your internet stability and try again."
    except Exception as e:
        print(f"{RED}[Network Error]: {e}{RESET}")
        return "Network connection issue detected. Unable to reach the AI engine."

def get_battery_metrics():
    """Pulls current charging, voltage, and health attributes via Termux JSON blocks."""
    try:
        raw_output = subprocess.check_output(["termux-battery-status"], text=True)
        json_data = json.loads(raw_output)
        return f"Battery level is at {json_data['percentage']}% and status is {json_data['status']}."
    except:
        return "Failed to retrieve device battery statistics."

def get_wifi_metrics():
    """Extracts internal wireless local area network configurations."""
    try:
        raw_output = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        json_data = json.loads(raw_output)
        if json_data.get("supplicant_state") == "COMPLETED":
            return f"Connected to Wi-Fi SSID: {json_data.get('ssid', 'Hidden')}."
        return "Device is not connected to any active Wi-Fi networks."
    except:
        return "Failed to interface with Wi-Fi hardware configurations."

def load_stored_profile():
    """Loads saved profiles directly from persistent disk configuration space."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as file_stream:
                return json.load(file_stream)
        except:
            return None
    return None

def save_profile_to_disk(gender):
    """Writes persistent profile configurations to local storage file."""
    profile_data = {"gender": gender}
    with open(CONFIG_FILE, 'w') as file_stream:
        json.dump(profile_data, file_stream, indent=4)

def run_onboarding_setup():
    """Quick onboarding script to determine user configuration parameters."""
    print(f"{YELLOW}[Setup Wizard Initialization]{RESET}")
    deliver_response("Please state or type your gender. Enter M for Male or F for Female.")
    
    gender_identity = "User"
    while True:
        raw_ans = get_user_input()
        if raw_ans:
            val = raw_ans.lower().strip()
            if val in ["m", "male", "mail", "man", "boy"]:
                gender_identity = "Male"
                break
            elif val in ["f", "female", "girl", "woman"]:
                gender_identity = "Female"
                break
        print(f"{RED}Invalid entry. Please try stating or typing your gender again.{RESET}")

    save_profile_to_disk(gender_identity)
    deliver_response("User profile configuration saved successfully.")
    return gender_identity

if __name__ == "__main__":
    display_dynamic_banner()
    
    print(f"{YELLOW}Select Operational Input Interface Mode:{RESET}")
    print(f" [{GREEN}T{RESET}] Typing Keyboard Interface Mode (Silent)")
    print(f" [{GREEN}V{RESET}] Voice Speech Interface Mode (Audio Output)")
    
    while True:
        mode_token = input(f"\n{BLUE}Select Interface Mode [T/V]: {RESET}").lower().strip()
        if mode_token in ["t", "typing"]:
            selected_mode = "typing"
            print(f"{GREEN}[Typing Mode Activated]: System will remain silent.{RESET}")
            break
        elif mode_token in ["v", "voice"]:
            selected_mode = "voice"
            print(f"{GREEN}[Voice Mode Activated]: System audio output enabled.{RESET}")
            break
        print(f"{RED}Error: Choice not recognized. Enter 'T' or 'V'.{RESET}")

    stored_profile = load_stored_profile()
    if stored_profile:
        user_gender = stored_profile.get("gender", "User")
        print(f"{GREEN}[Profile Loaded]: Gender={user_gender} | Language=English{RESET}")
    else:
        user_gender = run_onboarding_setup()

    deliver_response("JANO AI Online. Ready for your commands.")

    while True:
        cmd_string = get_user_input()
        if not cmd_string:
            continue

        cmd_normalized = cmd_string.lower().strip()

        # ========================================================
        # SYSTEM OPERATIONS INTERFACES (Termux APIs)
        # ========================================================
        if cmd_normalized in ["battery", "status"]:
            deliver_response(get_battery_metrics())
            
        elif cmd_normalized in ["wifi", "network"]:
            deliver_response(get_wifi_metrics())
        
        elif cmd_normalized in ["torch on", "flashlight on"]:
            subprocess.run(["termux-torch", "on"])
            deliver_response("Flashlight turned on.")
            
        elif cmd_normalized in ["torch off", "flashlight off"]:
            subprocess.run(["termux-torch", "off"])
            deliver_response("Flashlight turned off.")

        elif cmd_normalized == "clipboard":
            try:
                clipboard_text = subprocess.check_output(["termux-clipboard-get"], text=True).strip()
                deliver_response(f"Clipboard content: {clipboard_text if clipboard_text else 'Empty'}")
            except:
                deliver_response("Unable to access device clipboard.")
                
        elif cmd_normalized in ["vibrate", "alert"]:
            deliver_response("Vibrating hardware system.")
            subprocess.run(["termux-vibrate", "-d", "1000"])

        elif cmd_normalized in ["stop", "exit", "quit"]:
            deliver_response("Shutting down JANO AI. Goodbye!")
            break

        # ========================================================
        # STABLE CORE AI INFERENCE FASTRUN
        # ========================================================
        else:
            ai_inference_response = query_optimized_ai(cmd_string, user_gender)
            deliver_response(ai_inference_response)
        
        time.sleep(0.1)

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
    """Generates and displays stylized, randomized terminal arts."""
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
    print(banner_block)
    print(f"{accent_color}========================================================")
    print(f"                ENGINE DEVELOPED BY YOSEPH ALGANEH     ")
    print(f"========================================================{RESET}\n")

def respond(text, input_mode):
    """Handles responses smartly: Speaks ONLY in voice mode, Prints in both."""
    print(f"\n{CYAN}[JANO_AI]: {text}{RESET}")
    if input_mode == "voice":
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

def query_optimized_ai(question, gender):
    """Highly stable, ultra-fast English-only AI inference."""
    system_prompt = f"You are JANO_AI, a highly smart assistant developed by Yoseph Alganeh. The User gender is {gender}. Crucial Rule: Always respond strictly in English. Keep answers direct, concise, and ultra-fast. Do not use bold markdown asterisks."
    
    safe_question = urllib.parse.quote(question)
    safe_system = urllib.parse.quote(system_prompt)
    
    # Using explicit fast model query to bypass server lag
    url = f"https://text.pollinations.ai/{safe_question}?system={safe_system}&model=openai&cache=false"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return f"Server is busy (Status {response.status_code}). Please try again."
    except requests.exceptions.RequestException:
        return "Network connection issue. Please check your internet or retry."

def get_battery_metrics():
    """Pulls current charging, voltage, and health attributes via Termux JSON blocks."""
    try:
        raw_output = subprocess.check_output(["termux-battery-status"], text=True)
        json_data = json.loads(raw_output)
        return f"Battery capacity is at {json_data['percentage']}% and status is {json_data['status']}."
    except:
        return "Unable to parse device battery attributes."

def get_wifi_metrics():
    """Extracts internal wireless local area network configurations."""
    try:
        raw_output = subprocess.check_output(["termux-wifi-connectioninfo"], text=True)
        json_data = json.loads(raw_output)
        if json_data.get("supplicant_state") == "COMPLETED":
            return f"Connected to Wi-Fi. Network SSID: {json_data.get('ssid', 'Hidden')}."
        return "Your device is not connected to any active Wi-Fi networks."
    except:
        return "Hardware interface failed to read Wi-Fi configurations."

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
    profile_data = {"gender": gender, "language": "English"}
    with open(CONFIG_FILE, 'w') as file_stream:
        json.dump(profile_data, file_stream, indent=4)

def run_onboarding_setup(input_mode):
    """Onboarding setup optimized for quick start."""
    print(f"{YELLOW}[Setup Wizard Initialization]{RESET}")
    
    respond("Please state or type your gender. Enter M for Male or F for Female.", input_mode)
    gender_identity = "Male"
    while True:
        raw_ans = get_user_input(input_mode)
        if raw_ans:
            val = raw_ans.lower().strip()
            if val in ["m", "male", "mail", "man", "boy"]:
                gender_identity = "Male"
                break
            elif val in ["f", "female", "girl", "woman"]:
                gender_identity = "Female"
                break
        print(f"{RED}Invalid input. Please enter M or F.{RESET}")

    save_profile_to_disk(gender_identity)
    respond("User setup configuration saved successfully.", input_mode)
    return gender_identity

if __name__ == "__main__":
    display_dynamic_banner()
    
    print(f"{YELLOW}Select Operational Input Interface Mode:{RESET}")
    print(f" [{GREEN}T{RESET}] Typing Keyboard Interface Mode")
    print(f" [{GREEN}V{RESET}] Voice Speech Interface Mode")
    
    selected_mode = "typing"
    while True:
        mode_token = input(f"\n{BLUE}Select Interface Mode [T/V]: {RESET}").lower().strip()
        if mode_token in ["t", "typing"]:
            selected_mode = "typing"
            break
        elif mode_token in ["v", "voice"]:
            selected_mode = "voice"
            break
        print(f"{RED}Error: Code not recognized. Enter 'T' or 'V'.{RESET}")

    stored_profile = load_stored_profile()
    if stored_profile:
        user_gender = stored_profile.get("gender", "Male")
        print(f"{GREEN}[Profile Loaded]: Gender={user_gender} | Language=English{RESET}")
    else:
        user_gender = run_onboarding_setup(selected_mode)

    respond("JANO AI Online. Ready for your commands.", selected_mode)

    while True:
        cmd_string = get_user_input(selected_mode)
        if not cmd_string:
            continue

        cmd_normalized = cmd_string.lower().strip()

        # ========================================================
        # SYSTEM OPERATIONS INTERFACES (Termux APIs)
        # ========================================================
        if cmd_normalized in ["battery", "status"]:
            respond(get_battery_metrics(), selected_mode)
            
        elif cmd_normalized in ["wifi", "network"]:
            respond(get_wifi_metrics(), selected_mode)
        
        elif cmd_normalized in ["torch on", "flashlight on"]:
            subprocess.run(["termux-torch", "on"])
            respond("Flashlight turned on.", selected_mode)
            
        elif cmd_normalized in ["torch off", "flashlight off"]:
            subprocess.run(["termux-torch", "off"])
            respond("Flashlight turned off.", selected_mode)

        elif cmd_normalized == "clipboard":
            try:
                clipboard_text = subprocess.check_output(["termux-clipboard-get"], text=True).strip()
                respond(f"Clipboard content: {clipboard_text if clipboard_text else 'Empty'}", selected_mode)
            except:
                respond("Unable to interface with device clipboard.", selected_mode)
                
        elif cmd_normalized in ["vibrate", "buzz"]:
            respond("Vibrating system hardware.", selected_mode)
            subprocess.run(["termux-vibrate", "-d", "1000"])

        elif cmd_normalized in ["stop", "exit", "quit"]:
            respond("Shutting down JANO AI. Goodbye!", selected_mode)
            break

        # ========================================================
        # STABLE CORE AI INFERENCE
        # ========================================================
        else:
            ai_inference_response = query_optimized_ai(cmd_string, user_gender)
            respond(ai_inference_response, selected_mode)
        
        time.sleep(0.1)

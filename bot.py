import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

TOKEN = os.getenv("TOKEN")

USERS_FILE = "users.txt"

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write(str(user_id) + "\n")
        return

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    save_user(user_id)

    keyboard = [
        [InlineKeyboardButton("⬇ ऐप डाउनलोड करें", url="https://sites.google.com/view/admod/hitmaal")],
        [InlineKeyboardButton("🔥 फीचर्स", callback_data="features")],
        [InlineKeyboardButton("🔐 प्राइवेसी", callback_data="privacy")],
        [InlineKeyboardButton("🆘 सपोर्ट", url="https://t.me/HitMaal_helper_Bot")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "🔥 *HitMaal में आपका स्वागत है!*\n\n"
        "✔ फ्री 18+ वेब सीरीज़\n"
        "✔ बिना Ads\n"
        "✔ 100% प्राइवेट\n"
        "✔ App Lock फीचर\n\n"
        "नीचे से ऑप्शन चुनें 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "features":
        query.edit_message_text(
            "🔥 *HitMaal Features:*\n\n"
            "✔ Free Web Series\n"
            "✔ No Ads\n"
            "✔ App Lock\n"
            "✔ Fast Streaming\n"
            "✔ Regular Updates",
            parse_mode="Markdown"
        )

    elif query.data == "privacy":
        query.edit_message_text(
            "🔐 *Privacy Guarantee*\n\n"
            "हम आपकी प्राइवेसी को सबसे ऊपर रखते हैं।\n"
            "✔ कोई डेटा लीक नहीं\n"
            "✔ App Lock\n"
            "✔ Secure Access",
            parse_mode="Markdown"
        )

def users(update: Update, context: CallbackContext):
    if not os.path.exists(USERS_FILE):
        count = 0
    else:
        with open(USERS_FILE, "r") as f:
            count = len(f.read().splitlines())

    update.message.reply_text(f"👥 Total Users: {count}")

def broadcast(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("❌ Use: /broadcast Your message")
        return

    message = " ".join(context.args)

    if not os.path.exists(USERS_FILE):
        update.message.reply_text("No users yet.")
        return

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    sent = 0
    for user_id in users:
        try:
            context.bot.send_message(chat_id=int(user_id), text=message)
            sent += 1
        except:
            pass

    update.message.reply_text(f"✅ Message sent to {sent} users.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("users", users))
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

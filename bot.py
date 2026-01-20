import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    keyboard = [
        [InlineKeyboardButton("⬇ ऐप डाउनलोड करें", url="https://sites.google.com/view/admod/hitmaal")],
        [InlineKeyboardButton("🔥 फीचर्स", callback_data="features")],
        [InlineKeyboardButton("🔐 प्राइवेसी", callback_data="privacy")],
        [InlineKeyboardButton("🆘 सपोर्ट", url="https://t.me/HitMaal_helper_Bot")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔥 *HitMaal में आपका स्वागत है!*\n\n"
        "✔ फ्री 18+ वेब सीरीज़\n"
        "✔ बिना Ads\n"
        "✔ 100% प्राइवेट\n"
        "✔ App Lock फीचर\n\n"
        "नीचे से ऑप्शन चुनें 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "features":
        await query.edit_message_text(
            "🔥 *HitMaal Features:*\n\n"
            "✔ Free Web Series\n"
            "✔ No Ads\n"
            "✔ App Lock\n"
            "✔ Fast Streaming\n"
            "✔ Regular Updates",
            parse_mode="Markdown"
        )

    elif query.data == "privacy":
        await query.edit_message_text(
            "🔐 *Privacy Guarantee*\n\n"
            "हम आपकी प्राइवेसी को सबसे ऊपर रखते हैं।\n"
            "✔ कोई डेटा लीक नहीं\n"
            "✔ App Lock\n"
            "✔ Secure Access",
            parse_mode="Markdown"
        )

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(USERS_FILE):
        count = 0
    else:
        with open(USERS_FILE, "r") as f:
            count = len(f.read().splitlines())

    await update.message.reply_text(f"👥 Total Users: {count}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Use: /broadcast Your message")
        return

    message = " ".join(context.args)

    if not os.path.exists(USERS_FILE):
        await update.message.reply_text("No users yet.")
        return

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    sent = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"✅ Message sent to {sent} users.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot started...")
    app.run_polling()

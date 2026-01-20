import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

USERS_FILE = "users.txt"
AGE_FILE = "age_verified.txt"

ADMIN_ID = 822510623  # Your Telegram ID

DOWNLOAD_LINK = "https://sites.google.com/view/admod/hitmaal"
SUPPORT_LINK = "https://t.me/HitMaal_helper_Bot"
CHANNEL_LINK = "https://t.me/hitmaal"  # CHANGE THIS

# ------------------ Utils ------------------

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

def verify_age(user_id):
    if not os.path.exists(AGE_FILE):
        return False

    with open(AGE_FILE, "r") as f:
        return str(user_id) in f.read().splitlines()

def save_age(user_id):
    with open(AGE_FILE, "a") as f:
        f.write(str(user_id) + "\n")

# ------------------ Menus ------------------

def main_menu():
    keyboard = [
        [InlineKeyboardButton("⬇ Download App", url=DOWNLOAD_LINK)],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("🔥 Features", callback_data="features")],
        [InlineKeyboardButton("ℹ About", callback_data="about")],
        [InlineKeyboardButton("⚠ Disclaimer", callback_data="disclaimer")],
        [InlineKeyboardButton("🆘 Support", url=SUPPORT_LINK)]
    ]
    return InlineKeyboardMarkup(keyboard)

# ------------------ Start ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    if not verify_age(user_id):
        keyboard = [
            [InlineKeyboardButton("✅ I am 18+", callback_data="age_yes")],
            [InlineKeyboardButton("❌ I am under 18", callback_data="age_no")]
        ]
        await update.message.reply_text(
            "🔞 This bot is for 18+ users only.\n\nAre you 18 or older?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text(
        "🔥 *Welcome to HitMaal!*\n\n"
        "✔ Free 18+ Web Series\n"
        "✔ No Ads\n"
        "✔ 100% Private\n"
        "✔ App Lock Feature\n\n"
        "Choose an option below 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ------------------ Buttons ------------------

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "age_yes":
        save_age(user_id)
        await query.edit_message_text(
            "✅ Age verified! Welcome to HitMaal.",
            reply_markup=main_menu()
        )

    elif query.data == "age_no":
        await query.edit_message_text("❌ Sorry, this bot is only for 18+ users.")

    elif query.data == "features":
        await query.edit_message_text(
            "🔥 *HitMaal Features:*\n\n"
            "✔ Free Web Series\n"
            "✔ No Ads\n"
            "✔ App Lock\n"
            "✔ Fast Streaming\n"
            "✔ Regular Updates",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    elif query.data == "about":
        await query.edit_message_text(
            "ℹ *About HitMaal*\n\n"
            "HitMaal is a free 18+ web series streaming app.\n"
            "Private, secure, and regularly updated.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    elif query.data == "disclaimer":
        await query.edit_message_text(
            "⚠ *Disclaimer*\n\n"
            "This app is for entertainment purposes only.\n"
            "All content belongs to their respective owners.\n"
            "We do not host any content.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

# ------------------ Admin Commands ------------------

async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Access denied.")
        return

    if not os.path.exists(USERS_FILE):
        count = 0
    else:
        with open(USERS_FILE, "r") as f:
            count = len(f.read().splitlines())

    await update.message.reply_text(f"👥 Total Users: {count}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Access denied.")
        return

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

# ------------------ Auto Replies ------------------

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if any(word in text for word in ["hi", "hello", "hey"]):
        await update.message.reply_text("Hello 👋 Welcome to HitMaal!", reply_markup=main_menu())

    elif "download" in text or "link" in text:
        await update.message.reply_text(f"⬇ Download here:\n{DOWNLOAD_LINK}", reply_markup=main_menu())

    elif "help" in text:
        await update.message.reply_text("Need help? Click Support 👇", reply_markup=main_menu())

    elif "app" in text:
        await update.message.reply_text("HitMaal is a free 18+ web series app 🔥", reply_markup=main_menu())

# ------------------ Run ------------------

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("Bot started...")
    app.run_polling()

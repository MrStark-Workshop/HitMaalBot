import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")
USERS_FILE = "users.txt"
ADMIN_ID = 822510623  # Your Telegram ID

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

def main_menu():
    keyboard = [
        [InlineKeyboardButton("⬇ Download App", url="https://sites.google.com/view/admod/hitmaal")],
        [InlineKeyboardButton("🔥 Features", callback_data="features")],
        [InlineKeyboardButton("🔐 Privacy", callback_data="privacy")],
        [InlineKeyboardButton("🆘 Support", url="https://t.me/HitMaal_helper_Bot")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

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
            "Your privacy is our top priority.\n"
            "✔ No data leaks\n"
            "✔ App Lock\n"
            "✔ Secure access",
            parse_mode="Markdown"
        )

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

# Auto Replies
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if any(word in text for word in ["hi", "hello", "hey"]):
        await update.message.reply_text("Hello 👋 Welcome to HitMaal!", reply_markup=main_menu())

    elif "download" in text or "link" in text:
        await update.message.reply_text(
            "⬇ Download HitMaal App here:\nhttps://sites.google.com/view/admod/hitmaal",
            reply_markup=main_menu()
        )

    elif "help" in text:
        await update.message.reply_text("Need help? Click Support 👇", reply_markup=main_menu())

    elif "app" in text:
        await update.message.reply_text("HitMaal is a free 18+ web series app 🔥", reply_markup=main_menu())

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("users", users))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("Bot started...")
    app.run_polling()

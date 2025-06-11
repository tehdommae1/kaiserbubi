import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

# Produkte (Beispiel)
PRODUCTS = {
    "prod1": {"name": "Produkt A", "price": "10€"},
    "prod2": {"name": "Produkt B", "price": "20€"},
}

LOGIN_FILE = "logins.txt"

def load_logins():
    with open(LOGIN_FILE, "r") as f:
        lines = f.read().strip().split("\n")
    return lines

def remove_login(login):
    logins = load_logins()
    logins.remove(login)
    with open(LOGIN_FILE, "w") as f:
        f.write("\n".join(logins))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for key, prod in PRODUCTS.items():
        keyboard.append([InlineKeyboardButton(f"{prod['name']} - {prod['price']}", callback_data=f"buy_{key}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Willkommen! Wähle dein Produkt:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("buy_"):
        product_key = data[4:]
        product = PRODUCTS.get(product_key)
        if not product:
            await query.edit_message_text("Produkt nicht gefunden.")
            return

        logins = load_logins()
        if not logins:
            await query.edit_message_text("Keine Logindaten mehr verfügbar.")
            return

        login = logins[0]
        remove_login(login)

        await query.edit_message_text(f"Bezahlung simuliert.\nHier sind deine Logindaten:\n\n{login}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Benutze /start um Produkte zu sehen.")

if __name__ == "__main__":
    import os
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        print("Bitte setze die Umgebungsvariable BOT_TOKEN mit deinem Bot-Token.")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot läuft...")
    app.run_polling()

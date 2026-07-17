import os
from threading import Thread

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)

# ==========================
# CONFIGURATION
# ==========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("La variable d'environnement TOKEN est introuvable.")

# ==========================
# FLASK (obligatoire pour Web Service Render)
# ==========================

web = Flask(__name__)

@web.route("/")
def home():
    return "ProfitBook Bot est en ligne !"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

# ==========================
# COMMANDES TELEGRAM
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = """
📖🚀 Bienvenue sur Trading Book Bot

Ton compagnon d'apprentissage pour découvrir le trading et développer tes connaissances étape par étape.

📈 Accède à des ressources structurées.

👇 Choisis une option :
"""

    clavier = InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Guide gratuit", callback_data="guide_gratuit")],
        [InlineKeyboardButton("🎓 Guide complet", callback_data="guide_complet")],
        [InlineKeyboardButton("💬 Assistance", callback_data="assistance")]
    ])

    with open("B92BD8BE-1DD1-433A-9D70-7C31B13040A2.png", "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=message,
            reply_markup=clavier
        )


async def boutons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "guide_gratuit":
        await query.message.reply_text(
            "📖 Guide gratuit\n\nDécouvre les bases du trading."
        )

    elif query.data == "guide_complet":
        await query.message.reply_text(
            "🎓 Formation ProfitBook\n\n25 modules complets de trading."
        )

    elif query.data == "assistance":
        await query.message.reply_text(
            "💬 Contacte notre équipe pour toute assistance."
        )


async def formation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 Formation ProfitBook\n\n25 modules de trading."
    )

# ==========================
# MAIN
# ==========================

def main():

    Thread(target=run_web, daemon=True).start()

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("formation", formation))
    application.add_handler(CallbackQueryHandler(boutons))

    print("✅ ProfitBook Bot lancé")

    application.run_polling()

if __name__ == "__main__":
    main()

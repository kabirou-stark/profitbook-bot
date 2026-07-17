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

        clavier = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎓 Obtenir le guide complet", callback_data="guide_complet")]
        ])

        with open("guide-gratuit.pdf .pdf", "rb") as pdf:
            await query.message.reply_document(
                document=pdf,
                caption="📖 Voici ton guide gratuit ! Bonne lecture.",
                reply_markup=clavier
            )

 elif query.data == "guide_complet":

    clavier = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ J'ai effectué le paiement", callback_data="paiement_effectue")],
        [InlineKeyboardButton("💬 Assistance", callback_data="assistance")]
    ])

    await query.message.reply_text(
        "🎓 *GUIDE COMPLET PROFITBOOK*\n\n"

        "💰 *Prix : 15 USDT*\n\n"

        "📌 *Moyens de paiement Binance*\n\n"

        "🟢 *USDT (BEP20)*\n"
        "`<0x71da433a66bb583dc984b1888bea773c7fbc7764>`\n\n"

        "🟡 *Bitcoin (BTC)*\n"
        "`<13V7bNc1TgwRAEc7b3h9xZUMdWaGBJ23u2>`\n\n"

        "🔵 *Ethereum (ETH)*\n"
        "`<0x71da433a66bb583dc984b1888bea773c7fbc7764>`\n\n"

        "⚠️ Après avoir effectué le paiement, cliquez sur le bouton "
        "*✅ J'ai effectué le paiement* puis envoyez la capture d'écran de la transaction.",

        parse_mode="Markdown",
        reply_markup=clavier
    )

elif query.data == "paiement_effectue":

    await query.message.reply_text(
        "✅ Merci pour votre paiement.\n\n"
        "📷 Veuillez maintenant envoyer une capture d'écran de votre transaction.\n\n"
        "Après vérification, le Guide Complet ProfitBook vous sera envoyé."
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

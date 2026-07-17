import os
from threading import Thread

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)


# ==========================
# CONFIGURATION
# ==========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("La variable d'environnement TOKEN est introuvable.")


ADMIN_ID = 5269002026

utilisateurs_en_attente = set()


# ==========================
# FLASK RENDER
# ==========================

web = Flask(__name__)


@web.route("/")
def home():
    return "ProfitBook Bot est en ligne !"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)



# ==========================
# START
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = """
📖🚀 Bienvenue sur ProfitBook

Ton compagnon d'apprentissage du trading.

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



# ==========================
# BOUTONS
# ==========================

async def boutons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()



    # GUIDE GRATUIT
    if query.data == "guide_gratuit":

        clavier = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎓 obtenir le guide complet",
                    callback_data="guide_complet"
                )
            ]
        ])


        with open("guide-gratuit.pdf .pdf", "rb") as pdf:

            await query.message.reply_document(
                document=pdf,
                caption="📖 Voici ton guide gratuit.",
                reply_markup=clavier
            )



    # GUIDE COMPLET
    elif query.data == "guide_complet":

        clavier = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✅ J'ai effectué le paiement",
                    callback_data="paiement_effectue"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 Assistance",
                    callback_data="assistance"
                )
            ]
        ])


        await query.message.reply_text(

            "🎓 *GUIDE COMPLET PROFITBOOK*\n\n"
            "💰 Prix : 15 USDT\n\n"

            "🟢 USDT (BEP20)\n"
            "`0x71da433a66bb583dc984b1888bea773c7fbc7764`\n\n"

            "🟡 Bitcoin (BTC)\n"
            "`13V7bNc1TgwRAEc7b3h9xZUMdWaGBJ23u2`\n\n"

            "🔵 Ethereum (ETH)\n"
            "`0x71da433a66bb583dc984b1888bea773c7fbc7764`\n\n"

            "Après paiement, clique sur le bouton ci-dessous puis envoie la capture.",

            parse_mode="Markdown",
            reply_markup=clavier
        )



    # CLIENT A PAYE
    elif query.data == "paiement_effectue":

        utilisateurs_en_attente.add(query.from_user.id)


        await query.message.reply_text(

            "✅ Merci pour votre paiement.\n\n"
            "📷 Envoyez maintenant la capture de votre transaction.\n\n"
            "Après vérification, votre guide complet sera envoyé."
        )



    # ASSISTANCE
    elif query.data == "assistance":

        clavier = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "💬 Contacter l'assistance",
                    url="https://t.me/bi_kakk"
                )
            ]
        ])


        await query.message.reply_text(
            "💬 Contactez notre assistance.",
            reply_markup=clavier
        )



    # VALIDATION ADMIN
    elif query.data.startswith("valider_"):

        user_id = int(query.data.split("_")[1])


        with open("guide-complet.pdf", "rb") as pdf:

            await context.bot.send_document(
                chat_id=user_id,
                document=pdf,
                caption=(
                    "🎓 Merci pour votre confiance.\n\n"
                    "Voici votre Guide Complet ProfitBook 📖"
                )
            )


        await query.message.reply_text(
            "✅ Guide envoyé au client."
        )



# ==========================
# RECEPTION CAPTURE PAIEMENT
# ==========================

async def recevoir_paiement(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id


    if user_id not in utilisateurs_en_attente:

        await update.message.reply_text(
            "⚠️ Cliquez d'abord sur "
            "✅ J'ai effectué le paiement."
        )

        return



    photo = update.message.photo[-1]


    clavier = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Valider et envoyer le guide",
                callback_data=f"valider_{user_id}"
            )
        ]
    ])



    await context.bot.send_photo(

        chat_id=ADMIN_ID,

        photo=photo.file_id,

        caption=(
            "📩 Nouvelle preuve de paiement\n\n"
            f"👤 Nom : {update.message.from_user.first_name}\n"
            f"🆔 ID : {user_id}"
        ),

        reply_markup=clavier
    )



    await update.message.reply_text(
        "✅ Capture reçue.\n\n"
        "Votre paiement sera vérifié."
    )



    utilisateurs_en_attente.remove(user_id)




# ==========================
# FORMATION
# ==========================

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

    application.add_handler(
        MessageHandler(filters.PHOTO, recevoir_paiement)
    )


    print("✅ ProfitBook Bot lancé")


    application.run_polling()



if __name__ == "__main__":
    main()

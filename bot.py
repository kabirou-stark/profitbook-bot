import os
import json
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


ADMIN_ID = 526900202


# ==========================
# COMPTEUR UTILISATEURS
# ==========================

USERS_FILE = "users.json"


try:
    with open(USERS_FILE, "r") as f:
        utilisateurs = set(json.load(f))

except:
    utilisateurs = set()



def sauvegarder_utilisateurs():

    with open(USERS_FILE, "w") as f:
        json.dump(list(utilisateurs), f)



# ==========================
# VARIABLES PAIEMENTS
# ==========================

utilisateurs_en_attente = set()



# ==========================
# START
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id


    # ENREGISTRE L'UTILISATEUR

    if user_id not in utilisateurs:

        utilisateurs.add(user_id)

        sauvegarder_utilisateurs()



    message = """
📖📖🚀 Bienvenue sur L’Académie du Trading
Du Débutant au Trader Rentable

Ton compagnon d’apprentissage pour découvrir le trading et développer tes connaissances étape par étape.

📈 Accède à des ressources structurées, apprends les bases essentielles et découvre les bonnes pratiques pour mieux comprendre les marchés financiers.

🎯 Ton parcours vers une meilleure maîtrise du trading commence maintenant.

👇 Choisis ton option ci-dessous :
"""


    clavier = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📖 Guide gratuit",
                callback_data="guide_gratuit"
            )
        ],
        [
            InlineKeyboardButton(
                "🎓 Guide complet",
                callback_data="guide_complet"
            )
        ],
        [
            InlineKeyboardButton(
                "📚 Voir le programme des 12 modules",
                callback_data="programme_12"
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ Pourquoi choisir cette formation ?",
                callback_data="pourquoi_formation"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Assistance",
                callback_data="assistance"
            )
        ]
    ])


    with open("B92BD8BE-1DD1-433A-9D70-7C31B13040A2.png", "rb") as photo:

        await update.message.reply_photo(
            photo=photo,
            caption=message,
            reply_markup=clavier
        )
        # ==========================
# STATISTIQUES UTILISATEURS
# ==========================

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    await update.message.reply_text(
        f"👥 Nombre total d'utilisateurs : {len(utilisateurs)}"
    )



# ==========================
# FORMATION
# ==========================

async def formation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎓 Formation ProfitBook\n\n"
        "25 modules de trading."
    )


# ==========================
# MAIN
# ==========================
from flask import Flask
from threading import Thread

app = Flask(__name__)


@app.route("/")
def home():
    return "ProfitBook Bot is running"


import os

def run_web():
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
def main():

    Thread(
        target=run_web,
        daemon=True
    ).start()

    from telegram.request import HTTPXRequest
    import logging

    logging.basicConfig(
        level=logging.INFO
    )

    request = HTTPXRequest(
        connect_timeout=60,
        read_timeout=120,
        write_timeout=120,
        pool_timeout=60,
    )


    application = (
        Application.builder()
        .token(TOKEN)
        .request(request)
        .build()
    )


    async def error_handler(update, context):

        logging.error(
            "Erreur dans le bot :",
            exc_info=context.error
        )


    application.add_error_handler(
        error_handler
    )


    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("formation", formation)
    )

    application.add_handler(
        CommandHandler("stats", stats)
    )


    application.add_handler(
        CallbackQueryHandler(boutons)
    )


    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            recevoir_paiement
        )
    )


    print("✅ ProfitBook Bot lancé")


    application.run_polling(
        poll_interval=1,
        timeout=60,
        drop_pending_updates=True
    )



if __name__ == "__main__":

    print("🚀 Démarrage du bot...")

    main()

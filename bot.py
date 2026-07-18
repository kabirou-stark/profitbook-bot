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
📖🚀 🚀 Bienvenue sur **L’Académie du Trading
Du Débutant au Trader Rentable**

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
            "📚 Voir le programme des 25 modules",
            callback_data="programme_25"
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
# BOUTONS
# ==========================

async def boutons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

clavier_guide = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "🎓 Obtenir le Guide Complet",
            callback_data="guide_complet"
        )
    ]
])

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
            "📚 Voir le programme des 25 modules",
            callback_data="programme_25"
        )
    ],
    [
        InlineKeyboardButton(
            "🔒 Paiement sécurisé",
            callback_data="paiement_securise"
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

    # POURQUOI CHOISIR CETTE FORMATION
    elif query.data == "pourquoi_formation":

        await query.message.reply_text(

            "⭐ Pourquoi choisir L’Académie du Trading ?\n\n"

            "Le trading demande une méthode claire, "
            "de la discipline et une bonne compréhension "
            "des marchés financiers.\n\n"

            "📖 Avec PROFITBOOK, vous découvrez un parcours "
            "structuré en 25 modules conçu pour apprendre "
            "progressivement.\n\n"

            "Vous allez apprendre :\n\n"

            "✅ Les bases essentielles du trading\n"
            "✅ L’analyse des marchés financiers\n"
            "✅ Les outils et méthodes d’un trader\n"
            "✅ La gestion du risque\n"
            "✅ La psychologie du trading\n\n"

            "🎓 Une formation organisée pour vous aider "
            "à comprendre le trading avec plus de clarté.\n\n"

            "📖 L’Académie du Trading\n"
            "Du Débutant au Trader Rentable"
        )
    # PROGRAMME DES 25 MODULES
    elif query.data == "programme_25":

        await query.message.reply_text(
 
)

            "📚 PROGRAMME COMPLET\n"
            "🎓 L’ACADÉMIE DU TRADING\n\n"

            "Un parcours structuré de 25 modules "
            "pour passer de débutant à trader avec "
            "de meilleures bases.\n\n"

            "━━━━━━━━━━━━━━\n"

            "📖 MODULE 1 : Les fondamentaux du trading\n"
            "• Comprendre le trading\n"
            "• Les marchés financiers\n"
            "• Le rôle d’un trader\n\n"

            "📖 MODULE 2 : Découverte des marchés\n"
            "• Forex, Crypto, Actions et indices\n"
            "• Fonctionnement des marchés\n\n"

            "📖 MODULE 3 : Les plateformes de trading\n"
            "• Choisir son environnement\n"
            "• Utiliser les outils essentiels\n\n"

            "📖 MODULE 4 : Analyse technique\n"
            "• Lire un graphique\n"
            "• Supports et résistances\n\n"

            "📖 MODULE 5 : Les indicateurs techniques\n"
            "• RSI, moyennes mobiles, tendances\n\n"

            "📖 MODULE 6 : Les stratégies de trading\n"
            "• Construire un plan de trading\n\n"

            "📖 MODULE 7 : Gestion du risque\n"
            "• Protéger son capital\n"
            "• Taille des positions\n\n"

            "📖 MODULE 8 : Psychologie du trader\n"
            "• Discipline et émotions\n\n"

            "📖 MODULE 9 à 15 :\n"
            "• Méthodes d’analyse avancées\n"
            "• Price Action\n"
            "• Gestion des entrées et sorties\n"
            "• Optimisation des stratégies\n\n"

            "📖 MODULE 16 à 20 :\n"
            "• Création d’un plan professionnel\n"
            "• Analyse complète des marchés\n"
            "• Amélioration des performances\n\n"

            "📖 MODULE 21 à 25 :\n"
            "• Niveau avancé\n"
            "• Organisation d’un trader sérieux\n"
            "• Mise en pratique finale\n\n"

            "━━━━━━━━━━━━━━\n"

            "🚀 L’Académie du Trading\n"
            "📖 PROFITBOOK\n"
            "Du Débutant au Trader Rentable"
        )
# PAIEMENT SÉCURISÉ
elif query.data == "paiement_securise":

    await query.message.reply_text(
        "🔒 PAIEMENT SÉCURISÉ\n\n"
        "Votre sécurité est notre priorité.\n\n"
        "✅ Les paiements sont vérifiés avant la livraison de votre guide.\n"
        "✅ Vos informations personnelles restent confidentielles.\n"
        "✅ Votre guide est envoyé uniquement après validation du paiement.\n"
        "✅ En cas de difficulté, notre assistance est disponible.\n\n"
        "🎓 Achetez en toute confiance.",
        reply_markup=clavier_guide
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

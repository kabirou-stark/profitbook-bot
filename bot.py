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
    📖📖🚀 Bienvenue dans L’Académie du Trading
Du Débutant au Trader Rentable

Vous souhaitez découvrir le trading, mais vous ne savez pas par où commencer ? Ou vous avez déjà essayé d’apprendre sans obtenir de véritables résultats ?

Vous êtes au bon endroit.

L’Académie du Trading a été conçue pour vous accompagner pas à pas, quel que soit votre niveau. Grâce à une méthode claire, progressive et structurée, vous développerez des bases solides pour mieux comprendre les marchés financiers et adopter les bonnes pratiques utilisées par les traders disciplinés.

📈 Ce que vous trouverez dans cette formation :

✅ Un parcours complet organisé en 25 modules faciles à suivre.

✅ Des explications simples et accessibles, même si vous débutez totalement.

✅ Les connaissances essentielles pour comprendre le fonctionnement des marchés financiers, des graphiques et des mouvements de prix.

✅ Les méthodes et outils indispensables pour analyser le marché avec plus de confiance.

✅ Les principes de gestion du risque afin d’apprendre à protéger votre capital et éviter les erreurs les plus fréquentes.

✅ Les bases de la psychologie du trader pour développer la discipline, la patience et une meilleure prise de décision.

🎯Avec PROFITBOOK, vous progressez étape par étape, sans être submergé par des informations inutiles, afin d’acquérir les compétences essentielles pour évoluer avec méthode et confiance.

🚀 Votre parcours vers une meilleure maîtrise du trading commence aujourd’hui.

👇 Choisissez une option ci-dessous pour commencer votre apprentissage.
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
            reply_markup=clavier,
            parse_mode="Markdown"
        )

# ==========================
# BOUTONS
# ==========================

async def boutons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # Bouton réutilisable
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

        with open("guide-gratuit.pdf .pdf", "rb") as pdf:
            await query.message.reply_document(
                document=pdf,
                caption="📖 Voici ton guide gratuit.",
                reply_markup=clavier_guide
            )

       # GUIDE GRATUIT
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
            """⭐ Pourquoi choisir L’Académie du Trading ?

Le trading ne consiste pas à acheter et vendre au hasard. Pour progresser durablement, il faut suivre une méthode claire, comprendre le fonctionnement des marchés et développer une véritable discipline.

C'est exactement l'objectif de L'Académie du Trading – PROFITBOOK.

Notre formation a été conçue pour accompagner aussi bien les débutants que les personnes ayant déjà quelques notions, grâce à un parcours structuré de 25 modules.

📖 Ce que vous allez apprendre :

✅ Les fondamentaux du trading
• Comprendre le trading.
• Découvrir les marchés financiers.
• Comprendre le rôle d'un trader.

✅ L'analyse des marchés
• Lire les graphiques.
• Identifier les tendances.
• Comprendre les mouvements des prix.

✅ Les outils et méthodes
• Utiliser les plateformes de trading.
• Découvrir les principaux indicateurs.
• Construire un plan de trading.

✅ La gestion du risque
• Protéger son capital.
• Gérer la taille des positions.
• Utiliser correctement Stop Loss et Take Profit.

✅ La psychologie du trader
• Développer la discipline.
• Contrôler les émotions.
• Éviter les erreurs des débutants.

🎯 Une formation organisée en 25 modules qui vous accompagne étape par étape pour acquérir des bases solides et comprendre les marchés financiers avec méthode.

🚀 PROFITBOOK – Du Débutant au Trader Rentable.
""",
            reply_markup=clavier_guide
        )

    # PROGRAMME DES 25 MODULES
    elif query.data == "programme_25":

        await query.message.reply_text(
            "📚 PROGRAMME COMPLET\n"
            "🎓 L’ACADÉMIE DU TRADING\n\n"
            "📖 Module 1 : Les fondamentaux du trading\n"
            "📖 Module 2 : Découverte des marchés\n"
            "📖 Module 3 : Les plateformes de trading\n"
            "📖 Module 4 : Analyse technique\n"
            "📖 Module 5 : Les indicateurs techniques\n"
            "📖 Module 6 : Les stratégies de trading\n"
            "📖 Module 7 : Gestion du risque\n"
            "📖 Module 8 : Psychologie du trader\n"
            "📖 Modules 9 à 15 : Analyse avancée\n"
            "📖 Modules 16 à 20 : Plan professionnel\n"
            "📖 Modules 21 à 25 : Niveau avancé",
            reply_markup=clavier_guide
        )

    # PAIEMENT SÉCURISÉ
    elif query.data == "paiement_securise":

        await query.message.reply_text(
            "🔒 PAIEMENT SÉCURISÉ\n\n"
            "Votre sécurité est notre priorité.\n\n"
            "✅ Les paiements sont vérifiés avant la livraison.\n"
            "✅ Vos informations restent confidentielles.\n"
            "✅ Le guide est envoyé uniquement après validation.\n"
            "✅ Assistance disponible en cas de besoin.",
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
            "⚠️ Cliquez d'abord sur ✅ J'ai effectué le paiement."
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

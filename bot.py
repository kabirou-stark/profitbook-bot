from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import os

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = """
📖 🚀 Bienvenue sur Trading Book Bot

Ton compagnon d’apprentissage pour découvrir le trading et développer tes connaissances étape par étape.

📈 Accède à des ressources structurées, apprends les bases essentielles et découvre les bonnes pratiques pour mieux comprendre les marchés financiers.

🎯 Ton parcours vers une meilleure maîtrise du trading commence maintenant.

👇 Choisis ton option :
"""

    boutons = [
        [InlineKeyboardButton("📖 Guide gratuit", callback_data="guide_gratuit")],
        [InlineKeyboardButton("🎓 Guide complet", callback_data="guide_complet")],
        [InlineKeyboardButton("💬 Assistance", callback_data="assistance")]
    ]

    clavier = InlineKeyboardMarkup(boutons)

    # Mets ton image dans le dépôt avec le nom image.png
    await update.message.reply_photo(
        photo=open("B92BD8BE-1DD1-433A-9D70-7C31B13040A2.png", "rb"),
        caption=message,
        reply_markup=clavier
    )


async def boutons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "guide_gratuit":
        await query.message.reply_text(
            """
📖 GUIDE GRATUIT

Découvre les bases du trading avec notre introduction gratuite.

Tu apprendras :
✅ Les bases des marchés
✅ Les premiers concepts du trading
✅ Les erreurs à éviter
"""
        )

    elif query.data == "guide_complet":
        await query.message.reply_text(
            """
🎓 GUIDE COMPLET

L'Académie du Trading contient 25 modules :

✅ Analyse technique
✅ Stratégies de trading
✅ Gestion du risque
✅ Psychologie du trader
✅ Méthodes professionnelles

Passe du niveau débutant à une meilleure maîtrise du trading.
"""
        )

    elif query.data == "assistance":
        await query.message.reply_text(
            """
💬 ASSISTANCE

Besoin d'aide ?

Contacte notre équipe pour toute question concernant la formation.
"""
        )


async def formation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
🎓 FORMATION PROFITBOOK

Formation complète en 25 modules.

Apprends le trading étape par étape.
"""
    )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("formation", formation))
    app.add_handler(CallbackQueryHandler(boutons))

    print("Bot ProfitBook lancé")

    app.run_polling()


if __name__ == "__main__":
    main()

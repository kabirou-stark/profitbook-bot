from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

imporimport os

TOKEN = os.getenv("8852909745:AAEPWNHFVXeHGYWX2UbEnE1EhMc7cuB5zqs")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
📖 Bienvenue sur ProfitBook

🎓 L'Académie du Trading
Du Débutant au Trader Rentable

Apprends le trading étape par étape avec notre formation professionnelle.

Commandes disponibles :
/formation
/modules
/prix
/acheter
"""
    await update.message.reply_text(message)


async def formation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
🎓 FORMATION PROFITBOOK

L'Académie du Trading contient 25 modules :

✅ Analyse technique
✅ Stratégies de trading
✅ Gestion du risque
✅ Psychologie du trader
✅ Méthodes professionnelles

Passe du niveau débutant à trader rentable.
"""
    )


async def modules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
📚 Les 25 modules ProfitBook :

Module 1 : Introduction au trading
Module 2 : Les bases des marchés
Module 3 : Lecture des graphiques
...
Module 25 : Devenir un trader autonome

Formation complète disponible après inscription.
"""
    )


async def prix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
💰 Prix de la formation ProfitBook :

🎓 L'Académie du Trading
Accès complet aux 25 modules.

Contacte-nous pour obtenir les modalités d'inscription.
"""
    )


async def acheter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
🚀 Pour acheter la formation :

1️⃣ Contacte notre équipe
2️⃣ Effectue le paiement
3️⃣ Reçois ton accès privé à la formation

Merci de rejoindre ProfitBook 📖
"""
    )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("formation", formation))
    app.add_handler(CommandHandler("modules", modules))
    app.add_handler(CommandHandler("prix", prix))
    app.add_handler(CommandHandler("acheter", acheter))

    print("Bot ProfitBook lancé")

    app.run_polling()


if __name__ == "__main__":
    main()

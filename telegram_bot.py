import os

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Hello! I'm a resume search bot. To get started use /help"
    )


async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "List of available commands:\n"
        "/start - Get started with the bot\n"
        "/help - List commands\n"
        "/sites - Select a site to search for vacancies\n"
        "/criteria - Указать критерии фильтрации\n"
        "/search - Начать поиск резюме"
    )


async def select_site(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Select a site to search for vacancies:\n"
        "work.ua/resumes/?page=1\n"
        "robota.ua/ru/candidates/all/ukraine"
    )


#async def set_criteria(update: Update, context: CallbackContext) -> None:
#    await update.message.reply_text(
#        "Specify filter criteria:\n" 'For example: "Python programmer"'
#    )


#async def search_resume(update: Update, context: CallbackContext) -> None:
#    await update.message.reply_text("Searching for resumes...")


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("sites", select_site))
    #application.add_handler(CommandHandler("criteria", set_criteria))
    #application.add_handler(CommandHandler("search", search_resume))

    application.run_polling()


if __name__ == "__main__":
    main()

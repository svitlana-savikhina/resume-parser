import csv
import os

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    ApplicationBuilder,
    MessageHandler,
    ConversationHandler,
    filters
)
from dotenv import load_dotenv
from candidate_filter import filter_candidates_by_keyword

KEYWORD, SITE = range(2)
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
        "/search - Search for candidates by keyword\n"
    )


async def select_site(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Select a site to search for vacancies:\n"
        "work.ua\n"
        "robota.ua"
    )


async def search(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Enter a keyword to filter candidates:")
    return KEYWORD


async def receive_keyword(update: Update, context: CallbackContext) -> None:
    context.user_data['keyword'] = update.message.text
    keyboard = [
        [KeyboardButton("work.ua"), KeyboardButton("robota.ua")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Select a site to search for vacancies:", reply_markup=reply_markup)
    return SITE


async def receive_site(update: Update, context: CallbackContext) -> None:
    keyword = context.user_data.get('keyword')
    site = update.message.text.strip().lower()

    if site == "work.ua":
        input_file_path = "work_ua_parser_with_scores/resumes_from_work_ua.csv"
        output_file_path = "work_ua_parser_with_scores/filtered_candidates_from_work_ua.csv"
    elif site == "robota.ua":
        input_file_path = "robota_ua_parser_with_scores/resumes_from_robota_ua.csv"
        output_file_path = "robota_ua_parser_with_scores/filtered_candidates_from_robota_ua.csv"
    else:
        await update.message.reply_text("Invalid site selected. Please enter 'work.ua' or 'robota.ua'.")
        return ConversationHandler.END

    filter_candidates_by_keyword(input_file_path, keyword, output_file_path)

    with open(output_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)
        if not rows:
            await update.message.reply_text("No candidates found with the given keyword.")
        else:
            for row in rows:
                await update.message.reply_text(", ".join(row))

    return ConversationHandler.END


def run_bot() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("sites", select_site))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("search", search)],
        states={
            KEYWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_keyword)],
            SITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_site)],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    run_bot()

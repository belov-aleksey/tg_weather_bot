"""
Запускает телеграм-бот с данными о погоде в РФ

"""

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler

from settings import API_TOKEN_TG
from api_weather import get_weather


async def print_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    textMessage = await get_weather(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=textMessage)

async def print_unknown_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def print_start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Напиши мне название города,\
     в котором хочешь узнать погоду. \n Пример: Москва")

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN_TG).build()

    start_handler = CommandHandler('start', print_start_bot)
    weather_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), print_weather)
    unknown_handler = MessageHandler(filters.COMMAND, print_unknown_response)

    application.add_handler(start_handler)
    application.add_handler(weather_handler)
    application.add_handler(unknown_handler)

    application.run_polling()

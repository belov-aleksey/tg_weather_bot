"""
Запускает телеграм-бот с данными о погоде

"""

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler

from loguru import logger

from settings import API_TOKEN_TG
from api_weather import get_weather

logger.add('app.log',  format="{time} {level} {message}", level="INFO")

async def print_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    textMessage = await get_weather(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=textMessage)

async def print_unknown_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def print_start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Напиши мне название города,\
     в котором хочешь узнать погоду. \nПример: Москва")

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN_TG).build()
    logger.info('Токен бота получен')

    start_handler = CommandHandler('start', print_start_bot)
    weather_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), print_weather)
    unknown_handler = MessageHandler(filters.COMMAND, print_unknown_response)

    application.add_handler(start_handler)
    application.add_handler(weather_handler)
    application.add_handler(unknown_handler)

    logger.info('Хэндлеры добавлены. Запуск бота...')
    application.run_polling()

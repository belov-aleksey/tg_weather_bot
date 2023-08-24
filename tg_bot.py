'''
Запускает телеграм-бот с данными о погоде

'''

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler

from token_parse import API_TOKEN_TG
from api_weather import get_weather


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    textMessage = await get_weather(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=textMessage)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Напиши мне название города,\
     в котором хочешь узнать погоду. \n Пример: Москва")

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN_TG).build()

    start_handler = CommandHandler('start', start)
    weather_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), weather)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(weather_handler)
    application.add_handler(unknown_handler)

    application.run_polling()

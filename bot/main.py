from telebot import TeleBot
from bot import handlers
from bot.config import TOKEN

bot = TeleBot(TOKEN)

handlers = handlers.register_handlers(bot)

def main():
    print("Бот запущен...")
    bot.infinity_polling()
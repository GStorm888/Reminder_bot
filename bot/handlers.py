from telebot import TeleBot, types
from bot.config import TOKEN
from db.db import Database
from essence import User, Reminder
import datetime


def register_handlers(bot:TeleBot):
    @bot.message_handler(commands=['test'])
    def handle_test(message):
        Database.create_table()
        all_users = Database.get_all_users()
        print(all_users)
        all_reminders = Database.get_all_reminder()
        print(all_reminders)


    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        message = call.message
        if call.data == "help":
            bot.delete_message(message.chat.id, message.message_id)
            handle_help(message)
            message = call.message

        if call.data == "monday":  # напоминание на пн
            bot.send_message(message.chat.id, """Хорошо, в Понедельник, в какие еще дни?""")
            processing_day(0)
        elif call.data == "tuesday":  # напоминание на вт
            bot.send_message(message.chat.id, """Хорошо, во Вторник, в какие еще дни?""")
            processing_day(1)
        elif call.data == "wednesday":  # напоминание на ср
            bot.send_message(message.chat.id, """Хорошо, в Среду, в какие еще дни?""")
            processing_day(2)
        elif call.data == "thursday":  # напоминание на чт
            bot.send_message(message.chat.id, """Хорошо, в Четверг, в какие еще дни?""")
            processing_day(3)
        elif call.data == "friday":  # напоминание на пт
            bot.send_message(message.chat.id, """Хорошо, в Пятницу, в какие еще дни?""")
            processing_day(4)
        elif call.data == "saturday":  # напоминание на сб
            bot.send_message(message.chat.id, """Хорошо, в Субботу, в какие еще дни?""")
            processing_day(5)
        elif call.data == "sunday":  # напоминание на вс
            bot.send_message(message.chat.id, """Хорошо, в Воскресенье, в какие еще дни?""")
            processing_day(6)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, """Хорошо, в какое время?""")
        bot.register_next_step_handler(message, processing_time_reminder)





    @bot.message_handler(commands=['start'])
    def handle_start(message):
        bot.send_message(message.chat.id, "Привет! Введи свое имя")
        bot.register_next_step_handler(message, register_user)

    def register_user(message):
        telegram_id = str(message.chat.id)
        user_name = message.text
        if Database.get_user_by_user_name(user_name) is not None and telegram_id != Database.get_user_by_user_name(user_name)[0].telegram_id:
            bot.send_message(message.chat.id, "пользователь с таким именем уже есть, введи другое")
            bot.register_next_step_handler(message, handle_start)
            return
        if Database.get_user_by_user_name(user_name) is None:
            user = User(user_name, telegram_id)
            Database.add_user(user)
        markup = types.InlineKeyboardMarkup()
        help_bttn = types.InlineKeyboardButton(text="help", callback_data="help")
        markup.add(help_bttn)
        bot.send_message(message.chat.id, "готово, показать команды?", reply_markup=markup)




        
    def handle_help(message):
        bot.send_message(message.chat.id, "вот все функции:")



    @bot.message_handler(commands=['add_reminder'])
    def add_reminder(message):
        markup = types.InlineKeyboardMarkup()

        monday = types.InlineKeyboardButton(text="📅🟦Понедельник", callback_data="monday")
        tuesday = types.InlineKeyboardButton(text="📅🟧Вторник", callback_data="tuesday")

        wednesday = types.InlineKeyboardButton(text="📅🟩 Среда", callback_data="wednesday")
        thursday = types.InlineKeyboardButton(text="📅🟥Четверг", callback_data="thursday")

        friday = types.InlineKeyboardButton(text="📅🟪Пятница", callback_data="friday")
        saturday = types.InlineKeyboardButton(text="📅🟫Суббота", callback_data="saturday")

        sunday = types.InlineKeyboardButton(text="📅⬛Воскресенье", callback_data="sunday")
        finish_reminder = types.InlineKeyboardButton(
        )

        markup.add(monday, tuesday)
        markup.add(wednesday, thursday)
        markup.add(friday, saturday)
        markup.add(sunday)

        bot.send_message(
            message.chat.id, "Выберите дни в которые нужны напоминания", reply_markup=markup
        )

    def processing_day(day_int):
        
    processing_time_reminder
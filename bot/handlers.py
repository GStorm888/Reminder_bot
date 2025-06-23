from telebot import TeleBot, types
from bot.config import TOKEN
from db.db import Database
from essence import User, Reminder
import datetime
import calendar

def register_handlers(bot:TeleBot):

    @bot.message_handler(commands=['test'])
    def handle_test(message):
        Database.create_table()
        all_users = Database.get_all_users()
        print(all_users)
        all_reminders = Database.get_all_reminder()
        print(all_reminders)
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, """клавиатура отчищена""", reply_markup=markup)



    @bot.callback_query_handler(func=lambda call: True)
    def callback_query_help(call):
        message = call.message
        if call.data == "help":
            bot.delete_message(message.chat.id, message.message_id)
            handle_help(message)



    @bot.callback_query_handler(func=lambda call: call.data in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
    def callback_query_add_reminder(call):
            message = call.message      
            global day_reminder
            if call.data == "monday":  # напоминание на пн
                bot.send_message(message.chat.id, """Хорошо, в Понедельник""")
                day_reminder = 0
            elif call.data == "tuesday":  # напоминание на вт
                bot.send_message(message.chat.id, """Хорошо, во Вторник""")
                day_reminder = 1
            elif call.data == "wednesday":  # напоминание на ср
                bot.send_message(message.chat.id, """Хорошо, в Среду""")
                day_reminder = 2
            elif call.data == "thursday":  # напоминание на чт
                bot.send_message(message.chat.id, """Хорошо, в Четверг""")
                day_reminder = 3
            elif call.data == "friday":  # напоминание на пт
                bot.send_message(message.chat.id, """Хорошо, в Пятницу""")
                day_reminder = 4
            elif call.data == "saturday":  # напоминание на сб
                bot.send_message(message.chat.id, """Хорошо, в Субботу""")
                day_reminder = 5
            elif call.data == "sunday":  # напоминание на вс
                bot.send_message(message.chat.id, """Хорошо, в Воскресенье""")
                day_reminder = 6
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, """В какое время?""")
            bot.register_next_step_handler(message, processing_time_reminder)


    @bot.callback_query_handler(func=lambda call: call.data in ["del_monday", "del_tuesday", "del_wednesday", "del_thursday", "del_friday", "del_saturday", "del_sunday"])
    def callback_query_del_reminder(call):
            message = call.message      
            global day_reminder
            if call.data == "del_monday":  # напоминание на пн
                bot.send_message(message.chat.id, """Хорошо, в Понедельник""")
                day_reminder = 0
            elif call.data == "del_tuesday":  # напоминание на вт
                bot.send_message(message.chat.id, """Хорошо, во Вторник""")
                day_reminder = 1
            elif call.data == "del_wednesday":  # напоминание на ср
                bot.send_message(message.chat.id, """Хорошо, в Среду""")
                day_reminder = 2
            elif call.data == "del_thursday":  # напоминание на чт
                bot.send_message(message.chat.id, """Хорошо, в Четверг""")
                day_reminder = 3
            elif call.data == "del_friday":  # напоминание на пт
                bot.send_message(message.chat.id, """Хорошо, в Пятницу""")
                day_reminder = 4
            elif call.data == "del_saturday":  # напоминание на сб
                bot.send_message(message.chat.id, """Хорошо, в Субботу""")
                day_reminder = 5
            elif call.data == "del_sunday":  # напоминание на вс
                bot.send_message(message.chat.id, """Хорошо, в Воскресенье""")
                day_reminder = 6
            bot.delete_message(message.chat.id, message.message_id)
            bot.register_next_step_handler(message, processing_day_reminder_del)


    @bot.callback_query_handler(func=lambda call:True)
    def callback_query_del_reminder_time(call):
        message = call.message
        for i in range(num):
            if call.data == f"del_{i}":
                global id_reminder
                id_reminder = i
                del_reminder_processing_time(message)
            bot.delete_message(message.chat.id, message.message_id)
                


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

        wednesday = types.InlineKeyboardButton(text="📅🟩Среда", callback_data="wednesday")
        thursday = types.InlineKeyboardButton(text="📅🟥Четверг", callback_data="thursday")

        friday = types.InlineKeyboardButton(text="📅🟪Пятница", callback_data="friday")
        saturday = types.InlineKeyboardButton(text="📅🟫Суббота", callback_data="saturday")

        sunday = types.InlineKeyboardButton(text="📅⬛Воскресенье", callback_data="sunday")

        markup.add(monday, tuesday)
        markup.add(wednesday, thursday)
        markup.add(friday, saturday)
        markup.add(sunday)

        bot.send_message(
            message.chat.id, "Выберите дни в которые нужны напоминания", reply_markup=markup
        )



    def request_time(message):
        bot.send_message(message.chat.id, """В какое время?""")
        bot.register_next_step_handler(message.chat.id, processing_time_reminder)


    def processing_time_reminder(message):
        global time_reminder
        time_reminder = message.text
        bot.send_message(message.chat.id, """как назвать?""")
        bot.register_next_step_handler(message, processing_text_reminder)


    def processing_text_reminder(message):
        global text_reminder
        text_reminder = message.text
        save_reminder(message)

    def save_reminder(message):
        telegram_id = str(message.chat.id)
        user = Database.get_user_by_telegram_id(telegram_id)
        reminder = Reminder(user.user_name, day_reminder, time_reminder, text_reminder)
        Database.add_reminder(reminder)
        bot.send_message(message.chat.id, "я записал и буду вам напоминать")


    @bot.message_handler(commands=['del_reminder'])
    def del_reminder(message):
        markup = types.InlineKeyboardMarkup()

        monday = types.InlineKeyboardButton(text="📅🟦Понедельник", callback_data="del_monday")
        tuesday = types.InlineKeyboardButton(text="📅🟧Вторник", callback_data="del_tuesday")

        wednesday = types.InlineKeyboardButton(text="📅🟩Среда", callback_data="del_wednesday")
        thursday = types.InlineKeyboardButton(text="📅🟥Четверг", callback_data="del_thursday")

        friday = types.InlineKeyboardButton(text="📅🟪Пятница", callback_data="del_friday")
        saturday = types.InlineKeyboardButton(text="📅🟫Суббота", callback_data="del_saturday")

        sunday = types.InlineKeyboardButton(text="📅⬛Воскресенье", callback_data="del_sunday")

        markup.add(monday, tuesday)
        markup.add(wednesday, thursday)
        markup.add(friday, saturday)
        markup.add(sunday)

        bot.send_message(
            message.chat.id, "Выберите дни в которые нужны напоминания", reply_markup=markup
        )

    def processing_day_reminder_del(message):
        reminders = Database.get_reminders_by_day(day_reminder)
        day_name = calendar.day_name[day_reminder]
        global num
        num = 0
        if reminders is None:
            bot.send_message(message.chat.id, f"нет напоминаний на выбраный день {day_name}")
            return
        for reminder in reminders:
            print_text = f"{day_name} - {reminder.time_reminder}"
            num += 1
            name_del = f"del_{num}"
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text="delete", callback_data=name_del)
            markup.add(button)
            bot.send_message(message.chat.id, print_text, reply_markup = markup)

    def del_reminder_processing_time(message):
        reminders = Database.get_reminders_by_day(day_reminder)
        Database.delete_reminder_by_user_name_day_time_reminder(reminders[id_reminder])
        bot.send_message(message.chat.id, "удалил")

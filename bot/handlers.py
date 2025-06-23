from telebot import TeleBot, types
from db.db import Database
from essence import User, Reminder
import datetime
import calendar
import time

def register_handlers(bot:TeleBot):

    def examination_date_type(user_time):
        time_format = "%H:%M"
        try:
            datetime.datetime.strptime(user_time, time_format)
            return True
        except:
            return False
    
    @bot.message_handler(commands=['test'])
    def test(message):
        if message.text == "🔙Назад" or message.text == "Назад":
            handle_button(message)
            return
        Database.create_table()
        all_users = Database.get_all_users()
        print(all_users)
        all_reminders = Database.get_all_reminder()
        print(all_reminders)
        # markup = types.ReplyKeyboardRemove()
        # bot.send_message(message.chat.id, """клавиатура отчищена""", reply_markup=markup)



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


    @bot.callback_query_handler(func=lambda call: call.data in ["delete_monday", "delete_tuesday", "delete_wednesday", "delete_thursday", "delete_friday", "delete_saturday", "delete_sunday"])
    def callback_query_delete_reminder(call):
        message = call.message      
        global day_reminder
        if call.data == "delete_monday":  # напоминание на пн
            bot.send_message(message.chat.id, """Хорошо, в Понедельник""")
            day_reminder = 0
        elif call.data == "delete_tuesday":  # напоминание на вт
            bot.send_message(message.chat.id, """Хорошо, во Вторник""")
            day_reminder = 1
        elif call.data == "delete_wednesday":  # напоминание на ср
            bot.send_message(message.chat.id, """Хорошо, в Среду""")
            day_reminder = 2
        elif call.data == "delete_thursday":  # напоминание на чт
            bot.send_message(message.chat.id, """Хорошо, в Четверг""")
            day_reminder = 3
        elif call.data == "delete_friday":  # напоминание на пт
            bot.send_message(message.chat.id, """Хорошо, в Пятницу""")
            day_reminder = 4
        elif call.data == "delete_saturday":  # напоминание на сб
            bot.send_message(message.chat.id, """Хорошо, в Субботу""")
            day_reminder = 5
        elif call.data == "delete_sunday":  # напоминание на вс
            bot.send_message(message.chat.id, """Хорошо, в Воскресенье""")
            day_reminder = 6
        bot.delete_message(message.chat.id, message.message_id)
        processing_day_reminder_delete(message)



    @bot.callback_query_handler(func=lambda call: call.data.startswith("del_"))
    def callback_query_delete_reminder_time(call):
        message = call.message
        global id_reminder, lst_reminder
        try:
            idx = int(call.data.replace("del_", ""))
            id_reminder = idx - 1
            delete_reminder_processing_time(message)
            bot.delete_message(message.chat.id, message.message_id)
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, "Ошибка удаления напоминания.")


    @bot.callback_query_handler(func=lambda call: call.data in ["help", "start", "add_reminder", "delete_reminder"])
    def callback_query_help(call):
        message = call.message
        if call.data == "help":
            bot.delete_message(message.chat.id, message.message_id)
            help(message)
        elif call.data == "start":
            bot.delete_message(message.chat.id, message.message_id)
            start(message)
        elif call.data == "add_reminder":
            bot.delete_message(message.chat.id, message.message_id)
            add_reminder(message)
        elif call.data == "delete_reminder":
            bot.delete_message(message.chat.id, message.message_id)
            delete_reminder(message)


    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "Привет! Введи свое имя")
        bot.register_next_step_handler(message, register_user)

    def register_user(message):
        telegram_id = str(message.chat.id)
        user_name = message.text
        if Database.get_user_by_user_name(user_name) is not None and telegram_id != Database.get_user_by_user_name(user_name).telegram_id:
            bot.send_message(message.chat.id, "пользователь с таким именем уже есть, введи другое")
            bot.register_next_step_handler(message, start)
            return
        if Database.get_user_by_user_name(user_name) is None:
            user = User(user_name, telegram_id)
            Database.add_user(user)
        markup = types.InlineKeyboardMarkup()
        help_bttn = types.InlineKeyboardButton(text="help", callback_data="help")
        markup.add(help_bttn)
        bot.send_message(message.chat.id, "готово, показать команды?", reply_markup=markup)
        start_help_back_button(message)


    # появление кнопки '🔙Назад'
    def start_help_back_button(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("🔙Назад")
        markup.add(back)
        bot.send_message(
            message.chat.id,
            "Чтобы откуда угодно попасть в Help, просто нажмите на кнопку '🔙Назад', или напишите слово 'Назад'",
            reply_markup=markup,
            )
        
    @bot.message_handler(
        func=lambda message: message.text == "🔙Назад" or message.text == "Назад"
    )
    def handle_button(message):
        bot.send_message(message.chat.id, "Хорошо, возвращаю вас в Help")
        help(message)

    @bot.message_handler(commands=['help'])
    def help(message):

        markup = types.InlineKeyboardMarkup()

        help_bttn = types.InlineKeyboardButton(text="🆘help", callback_data="help")
        start_bttn = types.InlineKeyboardButton(text="🚀start", callback_data="start")

        add_reminder_bttn = types.InlineKeyboardButton(
            text="📅✅Добавить Напоминание", callback_data="add_reminder"
        )
        delete_reminder_bttn = types.InlineKeyboardButton(
            text="📅❌Удалить Напоминание", callback_data="delete_reminder"
        )

        markup.add(help_bttn, start_bttn)
        markup.add(add_reminder_bttn)
        markup.add(delete_reminder_bttn)


        bot.send_message(
            message.chat.id,
            """📌 Команды для тренера:
    🆘help — Справка по командам
    🚀start — Запуск бота
    📅✅Добавить Напоминание — Добавить напоминание
    📅❌Удалить Напоминание — Удалить напоминание

                        """,
            reply_markup=markup,
        )


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
        if message.text == "🔙Назад" or message.text == "Назад":
            handle_button(message)
            return
        bot.send_message(message.chat.id, """В какое время?""")
        bot.register_next_step_handler(message.chat.id, processing_time_reminder)


    def processing_time_reminder(message):
        if message.text == "🔙Назад" or message.text == "Назад":
            handle_button(message)
            return
        global time_reminder
        time_reminder = message.text
        if not examination_date_type(time_reminder):
            bot.send_message(message.chat.id, "Не тот формат времени")
            bot.register_next_step_handler(message, processing_time_reminder)
            return None
    
        bot.send_message(message.chat.id, """как назвать?""")
        bot.register_next_step_handler(message, processing_text_reminder)


    def processing_text_reminder(message):
        if message.text == "🔙Назад" or message.text == "Назад":
            handle_button(message)
            return
        global text_reminder
        text_reminder = message.text
        save_reminder(message)

    def save_reminder(message):
        if message.text == "🔙Назад" or message.text == "Назад":
            handle_button(message)
            return
        telegram_id = str(message.chat.id)
        user = Database.get_user_by_telegram_id(telegram_id)
        reminder = Reminder(user.user_name, day_reminder, time_reminder, text_reminder)
        Database.add_reminder(reminder)
        bot.send_message(message.chat.id, "я записал и буду вам напоминать")


    @bot.message_handler(commands=['delete_reminder'])
    def delete_reminder(message):
        if message.text == "🔙Назад" or message.text == "Назад":
            handle_button(message)
            return
        markup = types.InlineKeyboardMarkup()

        monday = types.InlineKeyboardButton(text="📅🟦Понедельник", callback_data="delete_monday")
        tuesday = types.InlineKeyboardButton(text="📅🟧Вторник", callback_data="delete_tuesday")

        wednesday = types.InlineKeyboardButton(text="📅🟩Среда", callback_data="delete_wednesday")
        thursday = types.InlineKeyboardButton(text="📅🟥Четверг", callback_data="delete_thursday")

        friday = types.InlineKeyboardButton(text="📅🟪Пятница", callback_data="delete_friday")
        saturday = types.InlineKeyboardButton(text="📅🟫Суббота", callback_data="delete_saturday")

        sunday = types.InlineKeyboardButton(text="📅⬛Воскресенье", callback_data="delete_sunday")

        markup.add(monday, tuesday)
        markup.add(wednesday, thursday)
        markup.add(friday, saturday)
        markup.add(sunday)

        bot.send_message(
            message.chat.id, "Выберите дни в которые нужны напоминания", reply_markup=markup
        )

    def processing_day_reminder_delete(message):
        if message.text == "🔙Назад" or message.text == "Назад":
            handle_button(message)
            return
        telegram_id = str(message.chat.id)
        user = Database.get_user_by_telegram_id(telegram_id)
        reminders = Database.get_reminders_by_user_name_and_day(user.user_name, day_reminder) 
        day_name = calendar.day_name[day_reminder]
        global num_reminders
        num_reminders = 0
        global lst_reminder
        lst_reminder = []
        if reminders is None:
            bot.send_message(message.chat.id, f"нет напоминаний на выбраный день {day_name}")
            return
        for reminder in reminders:
            print_text = f"{day_name} - {reminder.time_reminder}"
            num_reminders += 1
            name_delete = f"del_{num_reminders}"
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text="delete", callback_data=name_delete)
            markup.add(button)
            bot.send_message(message.chat.id, print_text, reply_markup = markup)
            lst_reminder.append(reminder)

    def delete_reminder_processing_time(message):
        if message.text == "🔙Назад" or message.text == "Назад":
            handle_button(message)
            return
        telegram_id = str(message.chat.id)
        user = Database.get_user_by_telegram_id(telegram_id)
        reminders = Database.get_reminders_by_user_name_and_day(user.user_name, day_reminder) 
        reminder = reminders[id_reminder]
        Database.delete_reminder_by_user_name_day_time_reminder(reminder.user_name, reminder.day_reminder, reminder.time_reminder)
        bot.send_message(message.chat.id, "удалил")


def check_reminder_every_minutes(bot:TeleBot):
    while True:
        now = datetime.datetime.now()
        today = now.weekday()
        time_now = now.strftime("%H:%M")
        all_reminders = Database.get_all_reminder()
        if all_reminders is not None:
            for reminder in all_reminders:
                if (
                    int(reminder.day_reminder) == today
                    and reminder.time_reminder == time_now
                ):
                    user = Database.get_user_by_user_name(reminder.user_name)
                    bot.send_message(
                        user.telegram_id,
                        f"⏰Напоминание!{reminder.text_reminder}")
        time.sleep(60)
    
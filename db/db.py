import sqlite3
from essence import User, Reminder

class Database:
    SCHEMA = "db/schema.sql"
    DATABASE = "db/reminder.db"


    @staticmethod
    def execute(sql, params=()):
        connection = sqlite3.connect(Database.DATABASE, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute(sql, params)

        connection.commit()


    @staticmethod
    def create_table():
        with open(Database.SCHEMA) as schema_file:
            connection = sqlite3.connect(Database.DATABASE)
            cursor = connection.cursor()
            cursor.executescript(schema_file.read())
            connection.commit()
            connection.close()


    @staticmethod
    def add_user(user: User):
        Database.execute(
            "INSERT INTO users (user_name, telegram_id) VALUES (?, ?)",
            [
                user.user_name,
                user.telegram_id,
            ],
        )
        return True


    @staticmethod 
    def get_all_users():
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")

        all_users = cursor.fetchall()
        users = []
        for id, user_name, telegram_user_id in all_users:
            user = User(user_name, telegram_user_id, id)
            users.append(user)
        if len(users) == 0:
            return None
        return users
    
    @staticmethod 
    def get_user_by_telegram_id(telegram_id):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE telegram_id=?", [telegram_id])

        all_users = cursor.fetchall()
        users = []
        for id, user_name, telegram_user_id in all_users:
            user = User(user_name, telegram_user_id, id)
            users.append(user)
        if len(users) == 0:
            return None
        return users
    

    @staticmethod 
    def get_user_by_user_name(user_name):
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE user_name=?", [user_name])

        all_users = cursor.fetchall()
        users = []
        for id, user_name, telegram_user_id in all_users:
            user = User(user_name, telegram_user_id, id)
            users.append(user)
        if len(users) == 0:
            return None
        return users
    

    @staticmethod 
    def get_all_reminder():
        connection = sqlite3.connect(Database.DATABASE)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM reminders")

        all_reminders = cursor.fetchall()
        reminders = []
        for id, user_name, telegram_user_id in all_reminders:
            reminder = User(user_name, telegram_user_id, id)
            reminders.append(reminder)
        if len(reminders) == 0:
            return None
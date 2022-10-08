import sqlite3

# подключение и соединение с базой данных
connect = sqlite3.connect('database.db', check_same_thread=False)
cursor = connect.cursor()

import sqlite3
import connect_db
import config
import db_functions

# создание таблиц
connect_db.cursor.execute('''CREATE TABLE IF NOT EXISTS "users" (
    "id"    INTEGER NOT NULL,
    "login" TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id" AUTOINCREMENT)
);''')
connect_db.connect.commit()

connect_db.cursor.execute('''CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);''')
connect_db.connect.commit()

connect_db.cursor.execute('''CREATE TABLE IF NOT EXISTS "signs" (
	"id_user"	INTEGER,
	"id_category"	INTEGER,
	FOREIGN KEY("id_user") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("id_category") REFERENCES "categories"("id") ON DELETE CASCADE ON UPDATE CASCADE
);''')
connect_db.connect.commit()

# заполнение таблицы категории
for category in config.categories_arr:
    db_functions.addCategory(category)

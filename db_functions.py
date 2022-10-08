import connect_db

#поиск пользователя в базе по логину
def findUser(login):
    return connect_db.cursor.execute('SELECT * FROM users WHERE login=?', (login,)).fetchone()

# регистрация
def reg(login):
    if findUser(login) == None:
        connect_db.cursor.execute('INSERT INTO users(login) VALUES (?)', (login,))
        connect_db.connect.commit()

# список всех категорий
def allCategories():
    res = connect_db.cursor.execute('SELECT categories.name FROM categories').fetchall()
    return [*(x for t in res for x in t)]

# поиск категории в базе
def findCategory(category):
    return connect_db.cursor.execute('SELECT * FROM categories WHERE name=?', (category,)).fetchone()

# добавить категорию
def addCategory(category):
    if findCategory(category) == None:
        connect_db.cursor.execute('INSERT INTO categories(name) VALUES (?)', (category,))
        connect_db.connect.commit()

def isSign(user, category):
    return connect_db.cursor.execute('SELECT * FROM signs WHERE id_user=? AND id_category=?', (user, category,)).fetchone()

#подписаться
def subscribe(user, category):
    findCat = findCategory(category)
    if findCat != None:
        if isSign(user, findCat[0]) == None:
            connect_db.cursor.execute('INSERT INTO signs(id_user, id_category) VALUES (?, ?)', (user, findCat[0],))
            connect_db.connect.commit()
            return 'Подписка оформлена'
        else:
            return 'Вы уже подписаны на эту категорию'
    else:
        return 'Ошибка'

# отписаться
def unsubscribe(user, category):
    findCat = findCategory(category)
    if findCat != None:
        if isSign(user, findCat[0]) != None:
            connect_db.cursor.execute('DELETE FROM signs WHERE id_user=? AND id_category =?', (user, findCat[0],))
            connect_db.connect.commit()
            return 'Подписка отменена'
        else:
            return 'Вы уже отписаны от этой категории'
    else:
        return 'Ошибка'

# подписки
def signs(user):
    res = connect_db.cursor.execute('SELECT categories.name FROM signs INNER JOIN categories ON signs.id_category = categories.id WHERE id_user=?', (user,)).fetchall()
    return [*(x for t in res for x in t)]

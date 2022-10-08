import telebot
from telebot import types
import config
import requests
import db_functions

bot = telebot.TeleBot(config.token)
news = []


def convertList(list):
    str = ''
    for i in list:
        str += i + "\n"
    return str


def user(message):
    user_id = message.from_user.id
    user = db_functions.findUser(user_id)
    return user[0]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'Список команд: \n /help - Команды \n /start, /ctrl - Главное меню \n /allcats - Список всех категорий \n /mysigns - Ваши подписки')

@bot.message_handler(commands=['start', 'ctrl'])
def send_welcome(message):
    user_id = message.from_user.id
    db_functions.reg(user_id)

    id_user = user(message)

    if db_functions.signs(id_user) == []:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnsubscribe = types.KeyboardButton('Подписаться')
        markup.row(btnsubscribe)
        bot.send_message(message.chat.id, 'Чтобы просматривать новости подпишитесь на интересующие вас категории',
                         reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnnews = types.KeyboardButton('Новости')
        btnctrl = types.KeyboardButton('Управление подписками')
        markup.row(btnnews, btnctrl)
        bot.send_message(message.chat.id, 'Выберите действие:',
                         reply_markup=markup)


def send_news(message):
    id_user = user(message)
    signs = db_functions.signs(id_user)

    for sign in signs:
        news = []
        news_req = requests.get(
                f'https://newsapi.org/v2/top-headlines?apiKey={config.news_api_key}&category={sign}&pageSize=1')
        for i in news_req.json()['articles']:
            news.append([i['title'], i['publishedAt'], i['url']])
        # answer = ""
        for line in news:
            # answer += convertList(line)+"------------\n"
            # if (message.text == 'news'):
            bot.send_message(message.chat.id, convertList(line))


def ctrl(message):
    if (message.text == 'Новости'):
        send_news(message)
    if (message.text == 'Управление подписками'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnsubscribe = types.KeyboardButton('Подписаться')
        btnunsubscribe = types.KeyboardButton('Отписаться')
        markup.row(btnsubscribe, btnunsubscribe)
        bot.send_message(message.chat.id, 'Выберите действие:',
                         reply_markup=markup)


def sub_unsub(message):
    cats = db_functions.allCategories()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if (message.text == 'Подписаться'):
        for cat in cats:
            cat = types.KeyboardButton(cat)
            markup.add(cat)
        back = types.KeyboardButton('Назад')
        markup.add(back)
        bot.register_next_step_handler(message, sub_cat)
        bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=markup)
    if (message.text == 'Отписаться'):
        for cat in cats:
            cat = types.KeyboardButton(cat)
            markup.add(cat)
        back = types.KeyboardButton('Назад')
        markup.add(back)
        bot.register_next_step_handler(message, unsub_cat)
        bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup=markup)


@bot.message_handler(commands=['allcats'])
def my_signs(message):
    cats = db_functions.allCategories()
    bot.send_message(message.chat.id, f'Список всех категорий: \n{convertList(cats)}')


@bot.message_handler(commands=['mysigns'])
def my_signs(message):
    id_user = user(message)
    signs = db_functions.signs(id_user)
    bot.send_message(message.chat.id, f'Категории, на которые вы подписаны: \n{convertList(signs)}')


@bot.message_handler(content_types=['text'])
def a(message):
    if message.text == 'Назад':
        send_welcome(message)
    else:
        ctrl(message)
        sub_unsub(message)


def sub_cat(message):
    if message.text == 'Назад':
        send_welcome(message)
    else:
        id_user = user(message)
        bot.send_message(message.chat.id, db_functions.subscribe(id_user, message.text))
        bot.register_next_step_handler(message, sub_cat)


def unsub_cat(message):
    if message.text == 'Назад':
        send_welcome(message)
    else:
        id_user = user(message)
        bot.send_message(message.chat.id, db_functions.unsubscribe(id_user, message.text))
        bot.register_next_step_handler(message, unsub_cat)



bot.infinity_polling()

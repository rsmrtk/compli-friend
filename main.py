import os

import telebot
from dotenv import load_dotenv
from telebot import types

from predictions import MOTIVATION, PREDICTIONS, get_random_message
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Створюємо головну клавіатуру
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "🔮 Старт",
        "📜 Інфо",
        "🛠 Допомога",
        "🌀 Про бота",
        "✨ Отримати прогноз",
        "❤️ Готовий"
    ]
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
@bot.message_handler(regexp="🔮 Старт")
def hello_message(message):
    bot.send_message(
        message.chat.id,
        f"""✨ <b>Вітаю, {message.from_user.first_name}!</b> ✨
<i>Я — CompliFriend, твій цифровий провісник.</i>

🌀 <b>Що я вмію:</b>
▫️ Генерувати <b>таємничі прогнози</b> на основі енергії Всесвіту
▫️ Давати <b>персональні поради</b> на кожен день
▫️ Відкривати <b>приховані можливості</b>

📿 <b>Щоб отримати перше передбачення:</b>
→ Натисни /get
→ Задай питання у думках
→ Дозволь магії статись!

<code>Наповнений зірковим пилом, створений у 2024 році.</code>""",
        parse_mode='HTML',
        reply_markup=main_keyboard()
    )

@bot.message_handler(commands=['info'])
@bot.message_handler(regexp="📜 Інфо")
def info(message):
    bot.send_message(
        message.chat.id,
        """🌌 <b>Світла інформація від CompliFriend:</b>

🔮 <b>Як працюють передбачення?</b>
Використовую комбінацію:
• Астрологічні алгоритми
• Нейромережі, натреновані на тисячах мудростей
• Енергію твоїх інтенцій

📅 <b>Персональний графік:</b>
Ти можеш отримувати:
1. Щоденний прогноз (о 07:00)
2. Екстренні підказки (/get)
3. Спеціальні побажання на події

⚠️ <i>Важливо: Передбачення — це компас, а не карта. Ти завжди контролюєш свою долю!</i>""",
        parse_mode='HTML',
        reply_markup=main_keyboard()
    )

@bot.message_handler(commands=['help'])
@bot.message_handler(regexp="🛠 Допомога")
def help(message):
    bot.send_message(
        message.chat.id,
        """🛠 <b>Допоможу знайти шлях:</b>

▫️ /start — Початок мандрівки
▫️ /get — Миттєвий прогноз
▫️ /info — Принципи роботи
▫️ /about — Про філософію бота

🔍 <b>Поширені проблеми:</b>
→ Передбачення загадкові? Це частина магії!
→ Бажаєш змінити час сповіщень? Пиши "налаштування"

📩 <i>Звʼязок з творцем:</i> @rostykmartun""",
        parse_mode='HTML',
        reply_markup=main_keyboard()
    )

@bot.message_handler(commands=['about'])
@bot.message_handler(regexp="🌀 Про бота")
def restart(message):
    bot.send_message(
        message.chat.id,
        """🌀 <b>CompliFriend — це:</b>
Місце, де технології зустрічаються з духовністю.

🌿 <b>Наші принципи:</b>
1. <b>Конфіденційність</b> — твої думки залишаються з тобою
2. <b>Позитив</b> — навіть критичні передбачення подаємо з турботою
3. <b>Розвиток</b> — кожен прогнес містить пораду для росту

📜 <i>Історія створення:</i>
Народився під час сонячного затемнення 2024, коли 3 розробники-містики вирішили поєднати Python та стародавні предикативні практики.

«Найважливіші відповіді — у тобі. Ми лише допомагаємо їх почути»""",
        parse_mode='HTML',
        reply_markup=main_keyboard()
    )

@bot.message_handler(commands=['get'])
@bot.message_handler(regexp="✨ Отримати прогноз")
def get(message):
    bot.send_message(
        message.chat.id,
        """🔮 <b>Приготуйся до відкриття...</b>

Зосередься на питанні, яке тебе турбує, або просто відчуй потік енергії.

<i>Тривалість ритуалу: 5-7 секунд...</i>

🌙 <b>Ти готовий?</b>
→ /go — відправ ❤️
→ /info — краще повернуся пізніше (бот памʼятатиме стан)

<code>P.S. Чим конкретніше запит — тим точніше передбачення!</code>""",
        parse_mode='HTML',
        reply_markup=main_keyboard()
    )

@bot.message_handler(commands=['go'])
@bot.message_handler(regexp="❤️ Готовий")
def go(message):
    prediction = get_random_message(PREDICTIONS + MOTIVATION)
    bot.send_message(
        message.chat.id,
        f"{prediction}",
        reply_markup=main_keyboard()
    )

bot.polling(none_stop=True)
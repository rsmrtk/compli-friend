import os
import json
import threading
import time
from datetime import datetime
import pytz

import telebot
from dotenv import load_dotenv
from telebot import types

from predictions import MOTIVATION, PREDICTIONS, get_random_message

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "daily_users.json")

# Список користувачів для щоденних прогнозів
daily_users: set[int] = set()
daily_users_lock = threading.Lock()


def load_daily_users():
    """Ініціалізує список користувачів із файла (якщо він є)."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        with daily_users_lock:
            daily_users.update(int(uid) for uid in data)
        print(f"[daily] loaded {len(daily_users)} users")
    except FileNotFoundError:
        print("[daily] no daily_users.json found, starting empty")
    except Exception as e:
        print(f"[daily] failed to load daily users: {e}")


def save_daily_users():
    """Зберігає поточний список користувачів атомарно."""
    try:
        with daily_users_lock:
            data = sorted(daily_users)
        tmp_path = DATA_FILE + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp_path, DATA_FILE)
        print(f"[daily] saved {len(data)} users")
    except Exception as e:
        print(f"[daily] failed to save daily users: {e}")


def add_daily_user(chat_id: int) -> bool:
    """Додає користувача до розсилки та зберігає список; повертає True якщо був новий."""
    with daily_users_lock:
        if chat_id in daily_users:
            return False
        daily_users.add(chat_id)
    save_daily_users()
    return True


def remove_daily_user(chat_id: int) -> bool:
    """Видаляє користувача (наприклад, якщо заблокував бота)."""
    with daily_users_lock:
        removed = chat_id in daily_users
        daily_users.discard(chat_id)
    if removed:
        save_daily_users()
    return removed


load_daily_users()


# Створюємо головну клавіатуру
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "🔮 Старт",
        "💜 Готовий"
    ]
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
@bot.message_handler(regexp="🔮 Старт")
def hello_message(message):
    # Додаємо користувача до списку для щоденних прогнозів
    added = add_daily_user(message.chat.id)
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

🌅 <b>Щоденні прогнози:</b>
Кожного дня о 09:09 ти отримуватимеш магічне передбачення!

<code>Наповнений зірковим пилом</code>""",
        parse_mode='HTML',
        reply_markup=main_keyboard()
    )
    if added:
        bot.send_message(
            message.chat.id,
            "🗓 Тебе додано до щоденної розсилки (09:09).",
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
1. Щоденний прогноз (о 09:09)
2. Екстренні підказки /get
3. Спеціальні побажання на події

⚠️ <i>Важливо: Передбачення — це компас, а не карта. Ти завжди
контролюєш свою долю!</i>""",
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
Народився під час сонячного затемнення 2024, коли 3 розробники-містики
вирішили поєднати Python та стародавні предикативні практики.

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
→ Натисни "💜 Готовий"
→ /info — краще повернуся пізніше (бот памʼятатиме стан)

<code>P.S. Чим конкретніше запит — тим точніше передбачення!</code>""",
        parse_mode='HTML',
        reply_markup=main_keyboard()
    )


@bot.message_handler(commands=['go'])
@bot.message_handler(regexp="💜 Готовий")
def go(message):
    prediction = get_random_message(PREDICTIONS + MOTIVATION)
    bot.send_message(
        message.chat.id,
        f"{prediction}",
        reply_markup=main_keyboard()
    )


# Функція для надсилання щоденних прогнозів
def send_daily_predictions():
    """Відправляє щоденні прогнози о 09:09 за київським часом"""
    kyiv_tz = pytz.timezone('Europe/Kyiv')
    while True:
        now = datetime.now(kyiv_tz)
        # Перевіряємо чи зараз 09:09 за київським часом
        if now.hour == 9 and now.minute == 9:
            greeting_text = """🌅 <b>Доброго ранку!</b> 🌅

<i>Нехай цей день буде наповнений магією!</i> ✨"""

            # Відправляємо всім користувачам
            with daily_users_lock:
                users_to_notify = list(daily_users)
            for user_id in users_to_notify:
                try:
                    # Генеруємо УНІКАЛЬНЕ передбачення для кожного користувача
                    prediction = get_random_message(PREDICTIONS + MOTIVATION)

                    # Спочатку привітання
                    bot.send_message(
                        user_id,
                        greeting_text,
                        parse_mode='HTML'
                    )
                    # Потім саме передбачення
                    time.sleep(1)  # Невелика затримка між повідомленнями
                    bot.send_message(
                        user_id,
                        prediction,
                        reply_markup=main_keyboard()
                    )
                except Exception as e:
                    print(f"Помилка відправки користувачу {user_id}: {e}")
                    # Видаляємо користувача якщо бот заблокований
                    if "blocked" in str(e).lower():
                        if remove_daily_user(user_id):
                            print(f"[daily] user {user_id} removed (blocked)")

            # Чекаємо 60 секунд щоб не відправити повідомлення двічі
            time.sleep(60)
        else:
            # Перевіряємо кожні 30 секунд
            time.sleep(30)


# Запускаємо щоденні прогнози в окремому потоці
daily_thread = threading.Thread(target=send_daily_predictions, daemon=True)
daily_thread.start()

bot.polling(none_stop=True)

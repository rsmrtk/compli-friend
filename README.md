ComlyBot: Твій щоденний заряд позитиву
Що це?

ComlyBot - це дружній Telegram-бот, створений для того, щоб зробити твій день яскравішим. Кожного дня він надсилає персоналізовані натхненні повідомлення, які допоможуть тобі знайти внутрішню гармонію та зарядитися позитивною енергією.

Як це працює?

Генерація передбачень: Бот використовує алгоритми машинного навчання для створення унікальних передбачень для кожного користувача.
Планування відправки: Завдяки використанню бібліотеки python-telegram-bot та механізму планування, бот точно вчасно надсилає повідомлення.
Інтерфейс користувача: Простий та інтуїтивно зрозумілий інтерфейс дозволяє легко взаємодіяти з ботом.
Технології:

Python: Мова програмування для розробки бекенду.
Telegram Bot API: Для взаємодії з Telegram.
python-telegram-bot: Бібліотека Python для роботи з Telegram API.
(додати інші технології, якщо використовуються)


ComlyBot: Your Daily Dose of Positivity
What is it?

ComlyBot is a friendly Telegram bot designed to brighten your day. It provides personalized, inspiring messages daily to help you find inner harmony and positive energy.

How does it work?

Personalized predictions: The bot uses machine learning algorithms to generate unique and inspiring messages for each user.
Scheduled delivery: Thanks to the python-telegram-bot library and a scheduling mechanism, the bot delivers messages on time.
User-friendly interface: The bot's interface is simple and intuitive, making it easy to use.
Technologies:

Python: Backend programming language.
Telegram Bot API: For interacting with Telegram.
python-telegram-bot: Python library for working with the Telegram Bot API.
(add other technologies if used)

Docker / Deploy
1) Підготувати env
- Скопіюй `.env.example` у `.env` та заповни `BOT_TOKEN`.
- За потреби задай `REGISTRY_IMAGE=registry.example.com/namespace/compli-friend:latest`, щоб build/push йшов у твій registry.

2) Зібрати й запустити локально через Compose
- `docker compose build bot`
- `docker compose up -d bot`
- Логи: `docker compose logs -f bot`

3) Опублікувати в Docker Registry
- `docker login <registry-host>`
- `REGISTRY_IMAGE=<registry>/namespace/compli-friend:latest docker compose build bot`
- `REGISTRY_IMAGE=<registry>/namespace/compli-friend:latest docker compose push bot`

4) Деплой на Webdock (через docker compose)
- Скопіюй на сервер `docker-compose.yml` і `.env` (без секретів у git).
- На сервері: `REGISTRY_IMAGE=<registry>/namespace/compli-friend:latest docker compose pull bot`
- Запуск: `docker compose up -d bot`
- Оновлення: `docker compose pull bot && docker compose up -d bot`

# LLM Bot — Telegram AI Chat with Payments

Telegram-бот с Mini App интерфейсом для общения с несколькими LLM-моделями.  
Встроенная монетизация через **Telegram Stars** — пользователи платят за доступ прямо в Telegram.

---

## Возможности

- **Mini App** — красивый чат-интерфейс прямо внутри Telegram
- **5 моделей** на выбор (переключение без перезагрузки)
- **Оплата Telegram Stars** — разовый доступ, без внешних платёжных систем
- **Админ-панель** — управление пользователями через команды бота
- **Streaming** — ответы появляются в реальном времени
- **История** — контекст последних 20 сообщений

---

## Модели

| Модель | Описание |
|--------|----------|
| ⚡ `x-ai/grok-4.1-fast` | Быстрый, прямолинейный |
| 🔵 `anthropic/claude-3-haiku` | Точный, понимает контекст |
| 🟠 `qwen/qwen3-32b` | Логика и рассуждения |
| 🟡 `qwen/qwen3-30b-a3b` | MoE архитектура — быстрая и эффективная |
| 🟢 `qwen/qwen3-coder-flash` | Код и дебаггинг |

Все модели доступны через **[polza.ai](https://polza.ai/?referral=UjroZUQFMU)** — российский агрегатор LLM API.

---

## Стек

```
Python 3.11+
aiogram 3        — Telegram Bot framework
FastAPI          — API для Mini App
uvicorn          — ASGI сервер
openai SDK       — запросы к LLM
SQLite           — база пользователей
cloudflared      — HTTPS туннель (без домена)
PM2              — менеджер процессов
```

---

## Установка

### 1. Требования

- VPS с Python 3.11+
- Бот в [@BotFather](https://t.me/BotFather)
- API ключ [polza.ai](https://polza.ai)
- Node.js (для PM2)

### 2. Клонировать

```bash
git clone https://github.com/NickIBrody/LLM-bot.git
cd LLM-bot
```

### 3. Виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Настройка `.env`

```bash
cp .env.example .env
nano .env
```

```env
BOT_TOKEN=your_telegram_bot_token
POLZA_KEY=your_polza_ai_api_key
ADMIN_IDS=your_telegram_id
STARS_PRICE=25
API_PORT=3000
WEBAPP_URL=https://your-domain.com
```

> Свой Telegram ID узнай через [@userinfobot](https://t.me/userinfobot)

### 5. HTTPS для Mini App

**Вариант A — Cloudflare Tunnel (без домена, бесплатно):**

```bash
# Установить cloudflared
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | gpg --dearmor -o /usr/share/keyrings/cloudflare-main.gpg
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main" > /etc/apt/sources.list.d/cloudflared.list
apt update && apt install cloudflared

# Запустить туннель
cloudflared tunnel --url http://localhost:3000 &
# Скопировать выданный URL в .env -> WEBAPP_URL
```

**Вариант B — собственный домен + Let's Encrypt:**

```bash
apt install nginx certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
# Настроить nginx как reverse proxy на порт 3000
```

### 6. Запуск через PM2

```bash
npm install -g pm2

# Бот
pm2 start "venv/bin/python -m bot.main" --name llm-bot

# API
pm2 start "venv/bin/uvicorn api.server:app --host 0.0.0.0 --port 3000" --name llm-api

pm2 save
pm2 startup
```

---

## Структура проекта

```
LLM-bot/
├── bot/
│   ├── handlers/
│   │   ├── start.py      — /start, главное меню
│   │   ├── payment.py    — Telegram Stars оплата
│   │   ├── admin.py      — админ-команды
│   │   └── chat.py       — общение с AI
│   └── main.py           — запуск бота
├── api/
│   └── server.py         — FastAPI + SSE стриминг
├── public/
│   └── index.html        — Mini App интерфейс
├── config.py             — конфигурация из .env
├── db.py                 — SQLite база данных
├── requirements.txt
└── .env.example
```

---

## Админ-команды

| Команда | Описание |
|---------|----------|
| `/admin` | Панель управления |
| `/grant <id>` | Выдать доступ пользователю |
| `/revoke <id>` | Забрать доступ |
| `/addadmin <id>` | Сделать пользователя админом |
| `/myid` | Узнать свой Telegram ID |

---

## Монетизация

Бот использует **Telegram Stars** — нативную платёжную систему Telegram.  
Пользователи без доступа видят кнопку оплаты прямо в чате.  
После оплаты — доступ навсегда, никаких подписок.

Цена настраивается в `.env`:
```env
STARS_PRICE=25
```

Смотри статистику через `/admin`.

---

## API

| Эндпоинт | Метод | Описание |
|----------|-------|----------|
| `POST /api/chat` | POST | Стриминг ответа от LLM |
| `/` | GET | Mini App интерфейс |

**Пример запроса:**
```json
POST /api/chat
{
  "model": "x-ai/grok-4.1-fast",
  "messages": [
    {"role": "user", "content": "Привет!"}
  ]
}
```

---

## Лицензия

MIT — используй свободно, модифицируй, продавай.

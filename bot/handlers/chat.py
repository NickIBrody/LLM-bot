from aiogram import Router
from aiogram.types import Message
from openai import AsyncOpenAI
import config, db

router = Router()
client = AsyncOpenAI(base_url="https://polza.ai/api/v1", api_key=config.POLZA_KEY)

# Хранилище истории в памяти
_history: dict[int, list] = {}
_model: dict[int, str] = {}

@router.message(lambda m: m.text and not m.text.startswith("/"))
async def on_message(msg: Message):
    uid = msg.from_user.id

    if uid not in config.ADMIN_IDS and not db.has_access(uid):
        return await msg.answer("Для использования нужен доступ.\n\n/start")

    model = _model.get(uid, "x-ai/grok-4.1-fast")
    history = _history.setdefault(uid, [])
    history.append({"role": "user", "content": msg.text})
    if len(history) > 20:
        _history[uid] = history[-20:]

    await msg.bot.send_chat_action(msg.chat.id, "typing")

    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=history,
            max_tokens=1500,
        )
        reply = resp.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        await msg.answer(reply, parse_mode="Markdown")
    except Exception as e:
        await msg.answer("❌ Ошибка. Попробуй ещё раз.")
        print(e)

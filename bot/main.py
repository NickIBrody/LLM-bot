import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from bot.handlers import start, payment, admin, chat
import config

async def run():
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=None))
    dp = Dispatcher()

    dp.include_router(payment.router)
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(chat.router)

    print("Bot запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(run())

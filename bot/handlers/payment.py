import time
from aiogram import Router, Bot
from aiogram.types import (
    CallbackQuery, Message, LabeledPrice,
    PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
)
import db, config

router = Router()

@router.callback_query(lambda c: c.data == "buy")
async def cb_buy(cb: CallbackQuery, bot: Bot):
    await cb.answer()
    await bot.send_invoice(
        chat_id=cb.from_user.id,
        title="Доступ к AI Chat",
        description="Разовая оплата - доступ навсегда ко всем моделям",
        payload="access_payment",
        currency="XTR",
        prices=[LabeledPrice(label="Доступ", amount=config.STARS_PRICE)],
    )

@router.pre_checkout_query()
async def pre_checkout(pcq: PreCheckoutQuery):
    await pcq.answer(ok=True)

@router.message(lambda m: getattr(m, "successful_payment", None) is not None)
async def on_payment(msg: Message, bot: Bot):
    uid = msg.from_user.id
    db.upsert(uid, paid_at=int(time.time()), stars=config.STARS_PRICE)
    db.grant(uid, "payment")

    webapp_url = config.get_webapp_url()
    await msg.answer(
        "✅ Оплата получена!\n\nДоступ открыт навсегда.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Открыть чат", web_app=WebAppInfo(url=webapp_url))]
        ])
    )

    for admin_id in config.ADMIN_IDS:
        try:
            u = msg.from_user
            await bot.send_message(
                admin_id,
                f"💰 Новая оплата!\n{u.first_name} (@{u.username or '-'})\nID: `{uid}`",
                parse_mode="Markdown"
            )
        except:
            pass

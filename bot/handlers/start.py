from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, CallbackQuery
import db, config

router = Router()

def start_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть чат", web_app=WebAppInfo(url=config.get_webapp_url()))],
        [InlineKeyboardButton(text="О боте", callback_data="about")],
    ])

def pay_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Купить доступ — {config.STARS_PRICE} ⭐", callback_data="buy")],
    ])

@router.message(CommandStart())
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    name = msg.from_user.first_name or "друг"

    db.upsert(uid,
        name=msg.from_user.first_name,
        username=msg.from_user.username,
    )

    if uid in config.ADMIN_IDS or db.has_access(uid):
        await msg.answer(f"Привет, {name}!\n\nВыбери действие:", reply_markup=start_kb())
    else:
        await msg.answer(
            f"Привет, {name}!\n\nДоступ к боту стоит *{config.STARS_PRICE} ⭐*\n_Оплата разовая, доступ навсегда_",
            parse_mode="Markdown",
            reply_markup=pay_kb(),
        )

@router.callback_query(lambda c: c.data == "about")
async def cb_about(cb: CallbackQuery):
    lines = "\n".join(f"{m[icon]} *{m[name]}* — {m[desc]}" for m in config.MODELS.values())
    await cb.message.edit_text(
        f"*AI Chat Bot*\n\nМодели:\n\n{lines}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="‹ Назад", callback_data="back_start")]
        ])
    )
    await cb.answer()

@router.callback_query(lambda c: c.data == "back_start")
async def cb_back(cb: CallbackQuery):
    name = cb.from_user.first_name or "друг"
    await cb.message.edit_text(
        f"Привет, {name}!\n\nВыбери действие:",
        reply_markup=start_kb()
    )
    await cb.answer()

@router.message(lambda m: getattr(m, "text", None) == "/myid")
async def cmd_myid(msg: Message):
    await msg.answer(f"Твой ID: `{msg.from_user.id}`", parse_mode="Markdown")

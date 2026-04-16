from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import db, config

router = Router()

def is_admin(uid): return uid in config.ADMIN_IDS

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="adm_users")],
        [InlineKeyboardButton(text="✅ Выдать доступ", callback_data="adm_grant"),
         InlineKeyboardButton(text="❌ Забрать", callback_data="adm_revoke")],
    ])

@router.message(Command("admin"))
async def cmd_admin(msg: Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("Нет доступа.")
    s = db.stats()
    await msg.answer(
        f"*Админ-панель*\n\nВсего: *{s[total]}*\nС доступом: *{s[active]}*\nОплатили: *{s[paid]}*",
        parse_mode="Markdown", reply_markup=admin_kb()
    )

@router.callback_query(lambda c: c.data == "adm_users")
async def cb_users(cb: CallbackQuery):
    if not is_admin(cb.from_user.id): return await cb.answer("Нет доступа.")
    await cb.answer()
    users = db.all_users()
    if not users:
        return await cb.message.answer("Нет пользователей.")
    lines = []
    for u in users[:30]:
        status = "✅" if u["access"] else "❌"
        uname = f"@{u[username]}" if u["username"] else ""
        n = u["name"] or "-"; lines.append(f"{status} {n} {uname}\n   `{u["id"]}`")
    await cb.message.answer(
        "*Пользователи:*\n\n" + "\n\n".join(lines),
        parse_mode="Markdown"
    )

@router.callback_query(lambda c: c.data == "adm_grant")
async def cb_grant_hint(cb: CallbackQuery):
    if not is_admin(cb.from_user.id): return await cb.answer()
    await cb.answer()
    await cb.message.answer("Введи: `/grant <user_id>`", parse_mode="Markdown")

@router.callback_query(lambda c: c.data == "adm_revoke")
async def cb_revoke_hint(cb: CallbackQuery):
    if not is_admin(cb.from_user.id): return await cb.answer()
    await cb.answer()
    await cb.message.answer("Введи: `/revoke <user_id>`", parse_mode="Markdown")

@router.message(Command("grant"))
async def cmd_grant(msg: Message, bot: Bot):
    if not is_admin(msg.from_user.id): return await msg.answer("Нет доступа.")
    parts = msg.text.split()
    if len(parts) < 2: return await msg.answer("Использование: /grant <user_id>")
    uid = int(parts[1])
    db.grant(uid, msg.from_user.id)
    await msg.answer(f"✅ Доступ выдан `{uid}`", parse_mode="Markdown")
    try: await bot.send_message(uid, "✅ Тебе выдан доступ!\n\n/start")
    except: pass

@router.message(Command("revoke"))
async def cmd_revoke(msg: Message):
    if not is_admin(msg.from_user.id): return await msg.answer("Нет доступа.")
    parts = msg.text.split()
    if len(parts) < 2: return await msg.answer("Использование: /revoke <user_id>")
    uid = int(parts[1])
    db.revoke(uid)
    await msg.answer(f"❌ Доступ забран у `{uid}`", parse_mode="Markdown")

@router.message(Command("addadmin"))
async def cmd_addadmin(msg: Message):
    if not is_admin(msg.from_user.id): return await msg.answer("Нет доступа.")
    parts = msg.text.split()
    if len(parts) < 2: return await msg.answer("Использование: /addadmin <user_id>")
    uid = int(parts[1])
    if uid not in config.ADMIN_IDS:
        config.ADMIN_IDS.append(uid)
    db.upsert(uid, is_admin=1)
    db.grant(uid, msg.from_user.id)
    await msg.answer(f"✅ `{uid}` теперь админ", parse_mode="Markdown")

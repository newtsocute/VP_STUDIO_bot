from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramForbiddenError
from .fsm import UserState
import aiosqlite
import logging

router = Router()

async def save_user(user_id: int):
    """Сохраняем пользователя в базу данных"""
    async with aiosqlite.connect("users.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    """Отправляем кнопку с подпиской + включаем FSM"""
    try:
        await save_user(message.from_user.id)

        subscribe_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="📢 Подписаться на канал", url="https://t.me/vp_test_bot_channel")]]
        )

        await message.answer(
            "👋 Здравствуйте!\n"
            "Вас приветствует VP-studio!\n"
            "Пожалуй, лучшая сеть салонов в Приморском крае! 🎀\n\n"
            "🎁 Подпишитесь на наш Telegram-канал, чтобы получить подарок, затем нажмите *✅ Проверить подписку*.",
            reply_markup=subscribe_keyboard,
            parse_mode="Markdown"
        )

        check_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subscription")]]
        )

        await message.answer("После подписки нажмите кнопку ниже:", reply_markup=check_keyboard)
        await state.set_state(UserState.waiting_for_subscription)

    except TelegramForbiddenError:
        logging.warning(f"🚫 Пользователь {message.from_user.id} заблокировал бота. Удаляем из базы.")
        await remove_user_from_db(message.from_user.id)
    except Exception as e:
        logging.error(f"❌ Ошибка в start: {e}")

async def remove_user_from_db(user_id: int):
    """Удаление пользователя из базы данных"""
    async with aiosqlite.connect("users.db") as db:
        await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await db.commit()

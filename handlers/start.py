from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from .fsm import UserState
import aiosqlite  # ✅ База данных для хранения пользователей

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
    await save_user(message.from_user.id)  # ✅ Сохраняем ID пользователя

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться на канал", url="https://t.me/vp_test_bot_channel")]
        ]
    )

    await message.answer(
        "👋 Привет! Чтобы получить 🎁 ПОДАРОК, подпишись на наш Telegram канал и нажми на кнопку ниже! 👇",
        reply_markup=keyboard
    )

    check_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text="✅ Проверить подписку")]]
    )

    await message.answer("После подписки нажмите '✅ Проверить подписку'", reply_markup=check_keyboard)
    await state.set_state(UserState.waiting_for_subscription)

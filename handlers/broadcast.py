from aiogram import Router, Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import aiosqlite
from config import ADMIN_CHAT_IDS

router = Router()

# ✅ Определяем FSM для рассылки
class BroadcastState(StatesGroup):
    waiting_for_message = State()

@router.message(Command("broadcast"))
async def ask_broadcast_message(message: types.Message, state: FSMContext):
    """Запрашиваем текст рассылки (только для админ-чата)"""
    chat_id = int(message.chat.id)
    expected_chat_id = int(ADMIN_CHAT_IDS)  # Преобразуем к `int`

    print(f"🔍 Полученный chat_id: {chat_id} (type={type(chat_id)})")
    print(f"🎯 Ожидаемый ADMIN_CHAT_ID: {expected_chat_id} (type={type(expected_chat_id)})")
    print(f"📢 Тип чата: {message.chat.type}")  # 🔥 Добавляем логирование типа чата

    if chat_id != expected_chat_id:
        return await message.answer("🚫 У вас нет доступа к этой команде!")

    await message.answer("✍ Введите сообщение для рассылки:")
    await state.set_state(BroadcastState.waiting_for_message)  # ✅ Устанавливаем состояние FSM

@router.message(BroadcastState.waiting_for_message)
async def send_broadcast(message: types.Message, state: FSMContext, bot: Bot):
    """Отправляем сообщение всем пользователям"""
    await state.clear()  # ✅ Очищаем состояние после ввода текста

    text = message.text
    sent_count = 0

    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            users = await cursor.fetchall()

            for user in users:
                user_id = user[0]
                try:
                    await bot.send_message(chat_id=user_id, text=text)
                    sent_count += 1
                except Exception as e:
                    print(f"❌ Ошибка отправки пользователю {user_id}: {e}")

    await message.answer(f"✅ Рассылка завершена! Сообщение отправлено {sent_count} пользователям.")

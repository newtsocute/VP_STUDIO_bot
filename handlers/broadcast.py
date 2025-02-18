from aiogram import Router, Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import aiosqlite
import re  # ✅ Для поиска URL в тексте
import logging  # ✅ Логирование
from config import ADMIN_CHAT_IDS

router = Router()

# ✅ Определяем FSM для рассылки
class BroadcastState(StatesGroup):
    waiting_for_message = State()

@router.message(Command("broadcast"))
async def ask_broadcast_message(message: types.Message, state: FSMContext):
    """Запрашиваем текст рассылки (только для админ-чата)"""
    chat_id = int(message.chat.id)
    expected_chat_id = int(ADMIN_CHAT_IDS)

    if chat_id != expected_chat_id:
        return await message.answer("🚫 У вас нет доступа к этой команде!")

    await message.answer("✍ Введите сообщение для рассылки.\n"
                         "Если хотите добавить кнопку с ссылкой, укажите URL в конце.\n\n"
                         "Пример:\n"
                         "`🔥 Сегодня скидки 50%! https://example.com`",
                         parse_mode="Markdown")

    await state.set_state(BroadcastState.waiting_for_message)

@router.message(BroadcastState.waiting_for_message)
async def send_broadcast(message: types.Message, state: FSMContext, bot: Bot):
    """Отправляем сообщение всем пользователям, удаляем тех, кто заблокировал бота"""
    await state.clear()

    text = message.text.strip()
    url_match = re.search(r"https?://\S+", text)
    url = url_match.group(0) if url_match else None
    text_without_url = text.replace(url, "").strip() if url else text

    reply_markup = (
        types.InlineKeyboardMarkup(
            inline_keyboard=[[types.InlineKeyboardButton(text="✅ Записаться", url=url)]]
        ) if url else None
    )

    sent_count = 0
    removed_count = 0  # ✅ Количество удалённых пользователей

    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            users = await cursor.fetchall()

            for user in users:
                user_id = user[0]
                try:
                    await bot.send_message(chat_id=user_id, text=text_without_url, reply_markup=reply_markup)
                    sent_count += 1
                except Exception as e:
                    error_text = str(e)
                    if "bot was blocked by the user" in error_text:
                        logging.warning(f"🚫 Пользователь {user_id} заблокировал бота. Удаляем из базы.")
                        await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                        await db.commit()
                        removed_count += 1
                    else:
                        logging.error(f"❌ Ошибка отправки пользователю {user_id}: {e}")

    await message.answer(f"✅ Рассылка завершена!\n📨 Отправлено: {sent_count}\n🗑 Удалено из базы: {removed_count}.")

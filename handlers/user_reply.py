from aiogram import Router, Bot, types
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError
import logging
from config import SUPPORT_CHAT_ID  # ✅ ID чата с менеджерами

router = Router()


@router.message(Command("m"))
async def send_admin_message(message: types.Message, bot: Bot):
    """📩 Отправка сообщения пользователю по команде `/m user_id текст` (Только в SUPPORT_CHAT_ID)"""

    # ✅ Проверяем, что команда отправлена **из SUPPORT_CHAT_ID**
    if message.chat.id != int(SUPPORT_CHAT_ID):  # 💡 Исправлено: сравнение с int
        return await message.answer("🚫 Эта команда доступна только в чате менеджеров.")

    parts = message.text.split(maxsplit=2)

    # ✅ Проверяем, есть ли все три части (команда, user_id, текст)
    if len(parts) < 3:
        return await message.answer("❌ Используйте: `/m user_id текст`", parse_mode="Markdown")

    user_id = parts[1]
    text = parts[2]

    # ✅ Проверяем, является ли `user_id` числом
    if not user_id.isdigit():
        return await message.answer("❌ Ошибка: user_id должен быть числом.")

    user_id = int(user_id)  # ✅ Преобразуем в число

    try:
        # ✅ Отправляем сообщение пользователю
        await bot.send_message(chat_id=user_id, text=f"{text}")
        await message.answer("✅ Сообщение успешно отправлено пользователю.")  # ✅ Подтверждение в чате менеджеров
    except TelegramForbiddenError:
        await message.answer("🚫 Пользователь заблокировал бота или не начал с ним диалог.")
    except Exception as e:
        logging.error(f"❌ Ошибка отправки сообщения пользователю {user_id}: {e}")
        await message.answer("❌ Ошибка при отправке сообщения.")

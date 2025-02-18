from aiogram import Router, Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
import logging
from config import SUPPORT_CHAT_ID  # ✅ ID чата менеджеров

router = Router()

@router.message()
async def forward_user_message(message: types.Message, bot: Bot, state: FSMContext):
    """📨 Пересылка сообщений пользователей в чат менеджеров (только после завершения FSM)"""

    # ✅ Проверяем текущее состояние FSM
    state_data = await state.get_state()
    if state_data is not None:
        return  # 💡 Если FSM активен – не пересылаем сообщение

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    text = message.text

    forward_text = (
        f"📨 *Новое сообщение от пользователя:*\n"
        f"👤 {user_name} (ID: `{user_id}`)\n\n"
        f"💬 {text}"
    )

    try:
        await bot.send_message(chat_id=int(SUPPORT_CHAT_ID), text=forward_text, parse_mode="Markdown")
    except TelegramForbiddenError:
        logging.warning("🚫 Чат менеджеров недоступен.")
    except Exception as e:
        logging.error(f"❌ Ошибка пересылки сообщения в чат менеджеров: {e}")

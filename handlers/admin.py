from aiogram import Router, Bot
from config import ADMIN_CHAT_IDS  # ✅ Используем один ID чата админов

router = Router()

async def notify_admin(bot: Bot, gift_choice: str, user_name: str, user_id: int, phone: str):
    """Отправляем данные о пользователе в админский чат"""
    text = (
        f"🚨 *Новый пользователь!* 📲\n"
        f"👤 *Имя:* {user_name}\n"
        f"🆔 *ID:* `{user_id}`\n"
        f"📞 *Телефон:* `{phone}`\n"
        f"🎁 *Выбранный подарок:* {gift_choice}"
    )

    try:
        print(f"📤 Отправляю сообщение в чат {ADMIN_CHAT_IDS}...")  # ✅ Логируем перед отправкой
        await bot.send_message(chat_id=ADMIN_CHAT_IDS, text=text, parse_mode="Markdown")
        print(f"✅ Уведомление успешно отправлено в чат: {ADMIN_CHAT_IDS}")
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения в {ADMIN_CHAT_IDS}: {e}")

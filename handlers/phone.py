from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from .admin import notify_admin
from .fsm import UserState
import re

router = Router()

async def ask_phone(message: types.Message, state: FSMContext):
    """Запрашиваем номер телефона"""
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[types.KeyboardButton(text="📱Жми сюда чтобы поделиться номером!", request_contact=True)]]
    )
    await message.answer(
        "📲 Пожалуйста, поделитесь своим номером телефона, нажмите на кнопку внизу",
        reply_markup=keyboard
    )
    await state.set_state(UserState.waiting_for_phone)


@router.message(UserState.waiting_for_phone, F.contact)
async def handle_contact(message: types.Message, state: FSMContext):
    """Сохраняем номер телефона (если отправили контакт)"""
    phone = message.contact.phone_number
    await process_phone_number(message, state, phone)


@router.message(UserState.waiting_for_phone, F.text)
async def handle_manual_phone(message: types.Message, state: FSMContext):
    """Обрабатываем номер телефона, введённый вручную"""
    phone = message.text.strip()

    # ✅ Проверяем, что номер введён в корректном формате
    if not re.match(r"^\+?[78][0-9]{10}$", phone):
        return await message.answer("❌ Пожалуйста, введите номер телефона в формате +79991234567 или 89991234567.")

    await process_phone_number(message, state, phone)


async def process_phone_number(message: types.Message, state: FSMContext, phone: str):
    """Сохраняем номер телефона и отправляем данные в админский чат"""
    user_id = message.from_user.id

    # ✅ Достаем все сохраненные данные из FSM
    user_data = await state.get_data()
    user_name = user_data.get("user_name", "Не указано")
    gift_choice = user_data.get("gift_choice", "Не выбран")

    # ✅ Отправляем все данные админу
    await notify_admin(message.bot, gift_choice, user_name, user_id, phone)

    await message.answer(
        "✅ Спасибо! Наш администратор свяжется с вами в ближайшее время! ❤️",
        reply_markup=types.ReplyKeyboardRemove()  # ❌ Убираем кнопку после получения номера
    )

    # ✅ Чистим состояние
    await state.clear()

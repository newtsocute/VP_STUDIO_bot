from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from .phone import ask_phone
from .fsm import UserState

router = Router()

@router.message(UserState.waiting_for_name, F.text)
async def save_name(message: types.Message, state: FSMContext):
    """Сохраняем имя и запрашиваем номер телефона"""
    await state.update_data(user_name=message.text)

    await ask_phone(message, state)  # ✅ Переходим к запросу номера телефона

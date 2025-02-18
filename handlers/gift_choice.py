from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from .fsm import UserState

router = Router()

# ✅ Список доступных подарков
AVAILABLE_GIFTS = ["🎀 Парафинотерапия", "💸 300₽ на любую услугу", "🎨 2000₽ на татуировку"]

async def choose_gift(message: types.Message, state: FSMContext):
    """Функция отправляет кнопки выбора подарка"""
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text=gift)] for gift in AVAILABLE_GIFTS]
    )

    await message.answer("🎁 Какой подарок Вы выберете?", reply_markup=keyboard)
    await state.set_state(UserState.waiting_for_gift_choice)


@router.message(UserState.waiting_for_gift_choice)
async def handle_gift_choice(message: types.Message, state: FSMContext):
    gift_choice = message.text.strip()

    # ✅ Проверяем, есть ли такой вариант
    if gift_choice not in AVAILABLE_GIFTS:
        return await message.answer("❌ Пожалуйста, выберите подарок из списка, используя кнопки ниже.\nЕсли не видите кнопки то сверните клавиатуру или нажмите на кнопку которая слева от голосовых сообщений.")

    # ✅ Сохраняем выбранный подарок в FSM
    await state.update_data(gift_choice=gift_choice)

    await message.answer("✍ Напишите своё имя:", reply_markup=ReplyKeyboardRemove())  # ❌ Убираем кнопки после выбора

    # ✅ Меняем состояние на ввод имени
    await state.set_state(UserState.waiting_for_name)

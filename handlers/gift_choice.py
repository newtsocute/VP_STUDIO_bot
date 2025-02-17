from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from .fsm import UserState

router = Router()

async def choose_gift(message: types.Message, state: FSMContext):
    """Функция отправляет кнопки выбора подарка"""
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="🎀 Парафинотерапия")],
            [KeyboardButton(text="💸 300₽ на любую услугу")],
            [KeyboardButton(text="🎨 2000₽ на татуировку")]
        ]
    )

    await message.answer("🎁 Какой подарок Вы выберете?", reply_markup=keyboard)
    await state.set_state(UserState.waiting_for_gift_choice)


@router.message(UserState.waiting_for_gift_choice,
                F.text.in_(["🎀 Парафинотерапия", "💸 300₽ на любую услугу", "🎨 2000₽ на татуировку"]))
async def handle_gift_choice(message: types.Message, state: FSMContext):
    gift_choice = message.text

    # ✅ Сохраняем выбранный подарок в FSM
    await state.update_data(gift_choice=gift_choice)

    await message.answer("✍ Напишите своё имя:")

    # ✅ Меняем состояние на ввод имени
    await state.set_state(UserState.waiting_for_name)

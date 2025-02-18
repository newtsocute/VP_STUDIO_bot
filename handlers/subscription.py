from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from config import CHANNEL_ID
from .gift_choice import choose_gift
from .fsm import UserState

router = Router()

@router.message(UserState.waiting_for_subscription, F.text == "✅ Проверить подписку")
async def check_subscription_text(message: types.Message, state: FSMContext):
    """Проверка подписки, если пользователь отправил текстовое сообщение"""
    await process_subscription_check(message, state, message.from_user.id)


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Проверка подписки, если пользователь нажал на инлайн-кнопку"""
    await process_subscription_check(callback_query.message, state, callback_query.from_user.id)
    await callback_query.answer()  # ✅ Закрываем callback-запрос


async def process_subscription_check(message: types.Message, state: FSMContext, user_id: int):
    """Функция проверки подписки"""
    try:
        member = await message.bot.get_chat_member(CHANNEL_ID, user_id)

        if member.status in ["member", "administrator", "creator"]:
            await message.answer("✅ Отлично! Вы подписаны!\nТеперь выберите ваш 🎁 подарок:")
            await choose_gift(message, state)  # ✅ Переход к выбору подарка
        else:
            await message.answer("🚫 Вы не подписаны! Пожалуйста, подпишитесь на канал и попробуйте снова.")

    except Exception as e:
        await message.answer("⚠️ Ошибка при проверке подписки. Попробуйте позже.")
        print(f"❌ Ошибка проверки подписки: {e}")

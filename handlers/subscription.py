from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from config import CHANNEL_ID
from .gift_choice import choose_gift
from .fsm import UserState

router = Router()


@router.message(UserState.waiting_for_subscription, F.text == "✅ Проверить подписку")
async def check_subscription(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        member = await message.bot.get_chat_member(CHANNEL_ID, user_id)

        if member.status in ["member", "administrator", "creator"]:
            await message.answer("✅ Отлично! Вы подписаны!\nТеперь выберите ваш 🎁 подарок:")

            # ✅ Вызов выбора подарка с передачей `state`
            await choose_gift(message, state)

        else:
            await message.answer("🚫 Вы не подписаны! Пожалуйста, подпишитесь на канал и попробуйте снова.")

    except Exception as e:
        await message.answer("⚠️ Ошибка при проверке подписки. Попробуйте позже.")
        print(f"Ошибка проверки подписки: {e}")

from aiogram.fsm.state import StatesGroup, State

class UserState(StatesGroup):
    waiting_for_subscription = State()
    waiting_for_gift_choice = State()
    waiting_for_name = State()
    waiting_for_phone = State()

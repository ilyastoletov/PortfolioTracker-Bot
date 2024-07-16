from aiogram.fsm.state import State, StatesGroup


class SessionState(StatesGroup):
    enter_password = State()
    authorized = State()
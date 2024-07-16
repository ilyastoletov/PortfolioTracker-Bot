from aiogram.fsm.state import State, StatesGroup


class AccountState(StatesGroup):
    network_name = State()
    address = State()
    initial_balance = State()
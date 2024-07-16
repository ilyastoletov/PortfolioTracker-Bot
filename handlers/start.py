import os
from aiogram import Router
from aiogram.types import Message
from message import messages
from state.session import SessionState
from aiogram.fsm.context import FSMContext
from keyboard.start import add_account_keyboard
from aiogram.filters.command import CommandStart, Command
from aiogram.filters.state import StateFilter

router = Router()


@router.message(CommandStart())
async def start_menu(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await msg.answer(messages.starting_message)
        await state.set_state(SessionState.enter_password)
    else:
        await msg.answer(messages.authorized_user_start)


@router.message(SessionState.enter_password)
async def check_password_correct(msg: Message, state: FSMContext):
    valid_password = os.getenv("PASSWORD")
    if msg.text == valid_password:
        await msg.delete()  # Delete the message with password to prevent leaking
        await msg.answer(messages.create_account_proposal, reply_markup=add_account_keyboard())
        await state.set_state(SessionState.authorized)
        await state.update_data(session="true")
    else:
        await msg.answer(messages.incorrect_password)


@router.message(StateFilter("*"), Command("cancel"))
async def reset_state(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    if state_data['session'] == 'true':
        await state.set_state(SessionState.authorized)
    else:
        await state.clear()
    await msg.answer(messages.state_cleared)

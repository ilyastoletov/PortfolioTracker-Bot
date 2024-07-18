from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from keyboard.account import available_networks_keyboard
from message import messages
from aiogram.fsm.context import FSMContext
from network.client import NetworkClient
from state.session import SessionState
from state.account import AccountState

router = Router()
router.message.filter(StateFilter(SessionState.authorized))

@router.callback_query(F.data == "create_account")
async def create_account_query(call: CallbackQuery, client: NetworkClient):
    await create_account_first_step(call.message, client)


@router.message(Command("new_account"))
async def create_account_first_step(msg: Message, client: NetworkClient, state: FSMContext):
    networks = await client.get_available_networks()
    await msg.answer(
        text=messages.account_first_step,
        reply_markup=available_networks_keyboard(networks),
        parse_mode="HTML"
    )
    await state.set_state(AccountState.network_name)

@router.callback_query(AccountState.network_name)
async def transfer_to_second_step(call: CallbackQuery, client: NetworkClient, state: FSMContext):
    address_tracking_networks = await client.get_address_tracking_networks()
    chosen_network = call.data
    await state.update_data(network_name=chosen_network)

    if chosen_network in address_tracking_networks:
        text = messages.account_optional_second_step
        await state.set_state(AccountState.address)
    else:
        text = messages.account_second_step
        await state.set_state(AccountState.initial_balance)

    await call.message.edit_text(text)


@router.message(AccountState.address)
async def handle_address(msg: Message, client: NetworkClient, state: FSMContext):
    state_data = await state.get_data()
    network = state_data['network']
    error = await client.create_account(
        network_name=network,
        address=msg.text,
        initial_balance=None
    )
    if error is not None:
        await msg.answer(f"Error: {error}")
    else:
        await show_account_created_message(msg, network, client)


@router.message(AccountState.initial_balance)
async def handle_initial_balance(msg: Message, client: NetworkClient, state: FSMContext):
    if not is_float(msg.text):
        await msg.answer(messages.numeric_reply_warning)
        return
    state_data = await state.get_data()
    network = state_data['network']
    error = await client.create_account(
        network_name=network,
        initial_balance=msg.text,
        address=None
    )
    if error is not None:
        await msg.answer(f"Error: {error}")
    else:
        await show_account_created_message(msg, network, client)

async def show_account_created_message(msg: Message, network_name: str, client: NetworkClient):
    pass

def is_float(v) -> bool:
    try:
        float(v)
        return True
    except Exception:
        return False
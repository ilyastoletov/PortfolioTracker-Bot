from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from network.client import NetworkClient
from state.session import SessionState

router = Router()
router.message.filter(StateFilter(SessionState.authorized))

@router.callback_query(F.data == "create_account")
async def create_account_query(call: CallbackQuery, client: NetworkClient):
    await create_account_first_step(call.message, client)


@router.message(Command("new_account"))
async def create_account_first_step(msg: Message, client: NetworkClient):
    networks = await client.get_available_networks()
    await msg.answer(str(networks))
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.types.bot_command import BotCommand
import asyncio
from network.client import NetworkClient
import logging

from handlers.start import router as session_router
from handlers.account import router as account_router
from handlers.error import router as error_router

async def set_bot_commands(bot: Bot):
    commands_list = [
        BotCommand(
            command="start",
            description="Start the bot"
        ),
        BotCommand(
            command="portfolio",
            description="Display your portfolio"
        ),
        BotCommand(
            command="new_account",
            description="Create a new account"
        ),
        BotCommand(
            command="accounts",
            description="See list of your accounts"
        ),
        BotCommand(
            command="new_tx",
            description="Add a transaction"
        ),
        BotCommand(
            command="tx_list",
            description="List of transactions"
        ),
    ]
    await bot.set_my_commands(commands_list)

async def main():
    load_dotenv()
    bot = Bot(os.getenv("BOT_KEY"))
    dp = Dispatcher()
    logging.basicConfig(level=logging.DEBUG)

    network_client = NetworkClient()

    dp.include_routers(session_router, account_router, error_router)
    dp['client'] = network_client

    try:
        await set_bot_commands(bot)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()

if __name__ == '__main__':
    asyncio.run(main())
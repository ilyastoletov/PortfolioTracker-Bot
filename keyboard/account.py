from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def available_networks_keyboard(networks: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in networks:
        builder.add(
            InlineKeyboardButton(text=item, callback_data=item)
        )
    builder.adjust(1)
    return builder.as_markup()
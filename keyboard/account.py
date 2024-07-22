from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton
)

def available_networks_keyboard(networks: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in networks:
        builder.add(
            InlineKeyboardButton(text=item, callback_data=item)
        )
    builder.adjust(1)
    return builder.as_markup()

def control_accounts_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Control accounts', callback_data='control_accounts_menu'))
    return builder.as_markup()

def control_account_menu(accounts: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for acc in accounts:
        builder.add(
            InlineKeyboardButton(text=acc, callback_data=acc)
        )
    builder.add(InlineKeyboardButton(text="Turn back ⬅️", callback_data='back'))
    builder.adjust(1)
    return builder.as_markup()

def control_account(has_address: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if has_address:
        builder.add(InlineKeyboardButton(text='Change address', callback_data="change_address"))
    builder.add(InlineKeyboardButton(text='Delete account', callback_data="delete"))
    builder.add(InlineKeyboardButton(text='Turn back ⬅️', callback_data='back'))
    builder.adjust(1)
    return builder.as_markup()

def address_cancel() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Cancel"))
    return builder.as_markup()

def confirm_delete() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Yes', callback_data="yes"),
        InlineKeyboardButton(text='No', callback_data="no"),
    )
    return builder.as_markup()

def remove_reply() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
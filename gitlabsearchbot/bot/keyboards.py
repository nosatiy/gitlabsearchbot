from aiogram import types
from bot.models import ObjectData


def get_keyboard(message: types.Message):
    pass
    callback_data_ignore_reg = ObjectData(
        target_string=message.text,
        action='cb_ignore_reg',
    ).pack()

    buttons = [
        [
            types.InlineKeyboardButton(text="Игнорировать регист", callback_data=callback_data_ignore_reg),
        ],
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def send_channel_btn(msg):
    desing = [
        [InlineKeyboardButton(f"User", url=f"{msg.from_user.url}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=desing, row_width=2)


def support_btn():
    desing = [
        [InlineKeyboardButton("Miraziz", url='https://t.me/Ken_Keneki'),
         InlineKeyboardButton('Mirahmad', url='https://t.me/MzMPrO')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=desing, row_width=2)

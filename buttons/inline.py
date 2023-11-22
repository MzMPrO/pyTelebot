from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def send_channel_btn(msg):
    desing = [
        [InlineKeyboardButton(text='✅Tastiqlash✅', callback_data='Tastiqlash'), InlineKeyboardButton(text='❌Bekor qilish❌', callback_data='Bekor qilish')],
        [InlineKeyboardButton(f"User", url=f"{msg.from_user.url}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=desing, row_width=2)

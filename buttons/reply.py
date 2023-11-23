from aiogram.types import ReplyKeyboardMarkup


def menu_btn():
    desing = [
        ["💸Steam ga pul otqazish💸", '🆘Support🆘'],
    ]
    return ReplyKeyboardMarkup(keyboard=desing, row_width=2, resize_keyboard=True)


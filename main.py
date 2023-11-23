import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InputFile

from backround import keep_alive
from buttons import *
from config import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


async def send_start_message(msg: types.Message):
    await msg.answer(f"Assalomu aleykum hurmatli {msg.from_user.full_name}. "
                     "Siz steam akauntizga pul otqazish botidasiz.")
    await msg.answer("Choose an option:", reply_markup=menu_btn())


@dp.message_handler(commands=['start'], state='*')
async def start_handler_wrapper(msg: types.Message, state: FSMContext):
    await send_start_message(msg)
    await state.finish()


@dp.message_handler(Text(equals="🆘Support🆘"))
async def request_balance_handler(msg: types.Message):
    await msg.answer("Agar nimadur savolila bosa supportga yozila.", reply_markup=support_btn())


@dp.message_handler(Text(equals="💸Steam ga pul otqazish💸"))
async def request_balance_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Iltimos steam akkauntizni ma'lumotini yuboring.")
    await state.set_state('chek_steam_state')


@dp.message_handler(state='chek_steam_state')
async def request_balance_handler(msg: types.Message, state: FSMContext):
    await state.update_data(steam=msg.text)
    await msg.answer("Iltimos qancha balansingizga tashashni summasini yuboring.\nMinimal 5.5$ va komisiya 9%")
    await state.set_state('chek_sum_state')


@dp.message_handler(state='chek_sum_state')
async def check_balance(msg: types.Message, state: FSMContext):
    try:
        balance = float(msg.text)
        if balance < 5.5:
            await msg.answer('Iltimis minimal 5.5$ summa kiritiladi.')
        else:
            await msg.answer("Iltimos chekni yuboring")
            await state.update_data(balance=balance)
            await state.set_state('send_chek_state')
    except ValueError:
        await msg.answer("Iltimos raqam kiriting.")


@dp.message_handler(state='send_chek_state', content_types=types.ContentTypes.ANY)
async def send_chek(msg: types.Message, state: FSMContext):
    if msg.photo:
        await process_photo(msg, state)
    else:
        await bot.send_message(msg.chat.id, "Iltimos rasm yuboring.")


async def process_photo(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    balance = data.get('balance')
    steam = data.get('steam')
    await state.finish()
    photo = msg.photo[-1]
    photo_file = await bot.get_file(photo.file_id)
    await photo_file.download()
    photo_path = photo_file.file_path

    with open(photo_path, 'rb') as photo_file:
        await bot.send_photo(CHANNEL_ID, InputFile(photo_file),
                             caption=f"<b>Steam:</b> {steam}\n<b>Tolangan Summa:</b> {balance}\n<b>Tolash Summasi</b>: {((balance * 91) / 100):.2f}$\nUser: <a href='{msg.from_user.url}'>{msg.from_user.full_name}</a>\nUser id: {msg.from_user.id}",
                             reply_markup=send_channel_btn(msg), parse_mode='HTML')

    os.remove(photo_path)
    await msg.reply(f"Chek tekshuruvga ketti.🕐\n24 soat atrofida {((balance * 91) / 100):.2f}$ steamga tushuriladi.")


keep_alive()


def start_bot():
    executor.start_polling(dp, skip_updates=True)

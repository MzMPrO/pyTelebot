import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text as Call_filter
from aiogram.types import InputFile
from buttons import *
from aiogram.dispatcher.filters import BoundFilter

API_TOKEN = '6516759967:AAEHM0fh5iQLSQ-U4Bxl_NWqyrhpdF8_o40'
CHANNEL_ID = -1002116744718
ADMIN_USER_ID = [976658539]
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class IsOwnerFilter(BoundFilter):
    key = "is_owner"

    def __init__(self, is_owner):
        self.is_owner = is_owner

    async def check(self, message: types.Message):
        return message.from_user.id in ADMIN_USER_ID


dp.filters_factory.bind(IsOwnerFilter)


async def ask_for_photo(msg):
    await bot.send_message(msg.chat.id, "Пожалуйста, отправьте фото.")


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await msg.answer("Привет! Я бот для отправки фото. Используй команду /send_photo.")


@dp.message_handler(is_owner=True, commands='admin')
async def send_welcome(msg: types.Message):
    await msg.answer("Привет! Я бот для отправки фото. Используй команду /admin.")


@dp.message_handler(commands=['send_photo'])
async def send_photo_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Pleasw send chek")
    await state.set_state('send_chek')


@dp.message_handler(content_types=types.ContentTypes.ANY, state='send_chek')
async def process_photo(msg: types.Message, state: FSMContext):
    if not msg.photo == []:
        photo = msg.photo[-1]
        photo_file = await bot.get_file(photo.file_id)
        await photo_file.download()
        photo_path = photo_file.file_path
        keyboard = send_channel_btn(msg)
        with open(photo_path, 'rb') as photo_file:
            await bot.send_photo(CHANNEL_ID, InputFile(photo_file),
                                 caption=f"Summa: 5$\nUser: <a href='{msg.from_user.url}'>{msg.from_user.full_name}</a>\nUser id: {msg.from_user.id}",
                                 reply_markup=keyboard, parse_mode='HTML')
        os.remove(photo_path)
        await msg.reply("Chek tekshuruvga ketti.🕐\n24 soat atrofida pulingiz steamga tushuriladi.")
        await state.finish()
    else:
        await ask_for_photo(msg)


@dp.callback_query_handler(Call_filter('Tastiqlash'))
async def call_check_succ_handler(c: types.CallbackQuery):
    await bot.send_message(chat_id=c.message.reply_markup.inline_keyboard[1][0].url.split('=', 1)[1],
                           text='<b>Tolovingiz tastiqlandi!!!</b>\nBir oz vaqt tan keyin steamga pulingizni otqizib beramiz.',
                           parse_mode='HTML')


@dp.callback_query_handler(Call_filter('Bekor qilish'))
async def call_check_succ_handler(c: types.CallbackQuery):
    await bot.send_message(chat_id=c.message.reply_markup.inline_keyboard[1][0].url.split('=', 1)[1],
                           text='<b>Sizning tolovingiz bekor qilindi!!!</b>\nSavolla: @MzMPrO, @Ken_Keneki.',
                           parse_mode='HTML')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp, skip_updates=True)

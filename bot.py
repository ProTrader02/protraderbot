import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Salom! Bot ishlayapti ✅")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import os
import asyncio
import asyncpg
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters import CommandStart, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from apirouter import datarequest
import dbmanager

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432")    
}

class OnRegistration(StatesGroup):
    name_waiting = State()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp_pool = None
pool = None
db = None

async def onbot_startup():
    global pool 
    pool = await asyncpg.create_pool(
        user='postgres',
        password='kvet',
        database='postgres',
        host='167.17.182.93'
    )

    global db
    db = dbmanager.DataBaseManager(pool)

async def onbot_end():
    None

@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    try:
        username = message.from_user.username
        tg_id = message.from_user.id

        if await db.CheckRegister(tg_id) == False:
            await db.AddUser(tg_id, username)

        if await db.IsHaveRealname(tg_id) == False:
            await state.get_state(OnRegistration.name_waiting)
            await message.answer(f"Привет, {username}. Мне нравится это имя, но скажи, как я могу тебя называть по-настоящему?")
        else:
            await message.answer(f"Снова привет. Ты меня перезапустил(а) и я готов считать твой рацион!")

    except Exception as error:
        print(error)


@dp.message(OnRegistration.name_waiting, F.text)
async def prompt_handler(message: types.Message, state: FSMContext):
    user_name = message.text
    tg_id = message.from_user.id
    
    await db.SetRealname(tg_id, user_name)

    await state.clear()

    await message.answer(f"Приятно познакомиться, {user_name}! Начнем считать твой рацион. Пиши, что ты съел(а) за день, а я подсчитаю суточные каллории.")

@dp.message(F.text)
async def prompt_handler(message: types.Message, state: FSMContext):
    try:
        username = message.from_user.username
        tg_id = message.from_user.id
        mess = message.text

        if await db.CheckRegister(tg_id) and await db.IsHaveRealname(tg_id):
            await message.answer(mess)

    except Exception as error:
        print(error)

async def main():
    dp.startup.register(onbot_startup)
    dp.shutdown.register(onbot_end)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
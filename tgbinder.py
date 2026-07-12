import os
import asyncio
import asyncpg
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters import CommandStart, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage 
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from apirouter import *
import dbmanager

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

class OnRegistration(StatesGroup):
    name_waiting = State()

class OnSetDailyAllow(StatesGroup):
    gender_waiting = State()
    weight_waiting = State()
    height_waiting = State()
    allow_awaiting = State()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp_pool = None
pool = None
db = None
storage = MemoryStorage()

def get_inline_gender_answer():
    girl = InlineKeyboardButton(text="Девушка🚺", callback_data="btn_girl")
    man = InlineKeyboardButton(text="Парень🚹", callback_data="btn_man")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[girl, man]])
    return keyboard

async def log_message_id(state: FSMContext, message_id: int):
    data = await state.get_data()

    msg_ids = data.get("messages_to_delete", [])
    msg_ids.append(message_id)

    await state.update_data(messages_to_delete=msg_ids)

async def OnPlusCallories(message, tg_id):
    answer = await datarequest(message)

    if answer != "None":
        if answer.isdigit():
            new_cal = int(answer)
            today_cal = await db.PlusTodayCal(tg_id, new_cal)

            if today_cal:
                return str(new_cal), str(today_cal)
            else:
                print("Неполадка в PlusTodayCal")
        else:
            print("Выдал не чисто число")
    else:
        print("Неполадка в apirouter")

async def onbot_startup():
    global pool 
    pool = await asyncpg.create_pool(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
    )

    global db
    db = dbmanager.DataBaseManager(pool)

async def onbot_end():
    None

@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    try:
        await state.clear()

        username = message.from_user.username
        tg_id = message.from_user.id

        if await db.CheckRegister(tg_id) == False:
            await db.AddUser(tg_id, username)

        if await db.IsHaveRealname(tg_id) == False:
            await state.set_state(OnRegistration.name_waiting)
            await message.answer(f"Привет, {username}. Мне нравится это имя, но скажи, как я могу тебя называть по-настоящему?")
        else:
            await message.answer(f"Снова привет. Ты меня перезапустил(а) и я готов считать твой рацион!")

    except Exception as error:
        print(error)

@dp.message(OnRegistration.name_waiting, F.text)
async def registr_waiting(message: types.Message, state: FSMContext):
    user_name = message.text
    tg_id = message.from_user.id
    
    await db.SetRealname(tg_id, user_name)

    await state.clear()
    await state.set_state(OnSetDailyAllow.gender_waiting)
    await message.answer(f"Приятно познакомиться, {user_name}! Ответь на пару легких вопросов")
    await log_message_id(state, message.message_id)

@dp.message(OnSetDailyAllow.gender_waiting, F.text)
async def allow_waiting(message: types.Message, state: FSMContext):
    await message.answer(
        "Укажите ваш пол.",
        reply_markup=get_inline_gender_answer()
    )
    await log_message_id(state, message.message_id)

@dp.callback_query(lambda c: c.data == "btn_man")
async def process_callback_man(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    await state.update_data(user_gender="Man")
    
    await callback_query.message.edit_text(
        text="Отлично!"
    )

    await state.set_state(OnSetDailyAllow.weight_waiting)

@dp.callback_query(lambda c: c.data == "btn_girl")
async def process_callback_man(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    await state.update_data(user_gender="Girl")
    
    await callback_query.message.edit_text(
        text="Отлично!"
    )

    await state.set_state(OnSetDailyAllow.weight_waiting)

@dp.message(OnSetDailyAllow.weight_waiting, F.text)
async def weight_waiting(message: types.Message, state: FSMContext):
    await log_message_id(state, message.message_id)

    await message.answer("Напиши свой вес числом.")
    await log_message_id(state, message.message_id)
    user_weight = message.text

    if user_weight.isdigit():
        await state.update_data(user_weight=user_weight)
        await state.set_state(OnSetDailyAllow.height_waiting)
    else:
        await message.delete()

@dp.message(OnSetDailyAllow.height_waiting, F.text)
async def height_waiting(message: types.Message, state: FSMContext):
    await log_message_id(state, message.message_id)
    await message.answer("Напиши свой рост числом.")
    await log_message_id(state, message.message_id)
    user_height = message.text

    if user_height.isdigit():
        await state.update_data(user_height=user_height)
        await state.set_state(OnSetDailyAllow.allow_awaiting)
    else:
        await message.delete()

@dp.message(OnSetDailyAllow.allow_awaiting, F.text)
async def allow_waiting(message: types.Message, state: FSMContext):
    id = message.from_user.id

    user_data = await state.get_data()
    all_data_prompt = f"{user_data.get("user_gender")} {user_data.get("user_weight") } {user_data.get("user_height")}"

    allow_cal = await dayallowrequest(all_data_prompt)

    if allow_cal.isdigit():
        # Удаление логированных сообщений
        msg_ids_to_delete = user_data.get("messages_to_delete", [])

        try:
            await bot.delete_messages(
                chat_id=message.chat.id, 
                message_ids=msg_ids_to_delete
            )
        except Exception as error:
            print(f"Ошибка при массовом удалении: {error}")
        #-------------------------------

        allow = await db.SetNewDailyAllow(id, allow_cal)
        await state.clear()
        await message.answer(f"""Отлично! Твоя дневная норма: {allow} каллорий🥕
                             Начнем считать твой рацион. Напиши что ты съел(а) за сегодня.""")

@dp.message(Command("todaycheck"))
async def cmd_todaycheck(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    answer = await db.GetTodayCal(tg_id)

    if answer:
        await message.answer(f"""Всего на сегодня: {str(answer)} каллорий ✅""")

@dp.message(F.text)
async def prompt_reading(message: types.Message, state: FSMContext):
    try:
        username = message.from_user.username
        tg_id = message.from_user.id
        prompt = message.text

        if prompt[0] != '/' and await db.CheckRegister(tg_id) and await db.IsHaveRealname(tg_id):
            answer = await OnPlusCallories(prompt, tg_id)

            if answer[0] and answer[1]:
                await message.answer(f"""Это вышло на {answer[0]} каллорий.
                                        Всего на сегодня: {answer[1]} каллорий ✅""")

    except Exception as error:
        print(error)

async def main():
    dp.startup.register(onbot_startup)
    dp.shutdown.register(onbot_end)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import logging

from keyboards.inline import *
from utils.logger import log_message_id, delete_log_message
from services.data_process import GetDayAllow

logger = logging.getLogger(__name__)

router = Router()

class OnRegistration(StatesGroup):
    name_waiting = State()

class OnSetDailyAllow(StatesGroup):
    gender_waiting = State()
    weight_waiting = State()
    height_waiting = State()

@router.message(OnRegistration.name_waiting, F.text)
async def registr_waiting(message: types.Message, state: FSMContext, db):
    user_name = message.text
    tg_id = message.from_user.id
    
    await db.SetRealname(tg_id, user_name)

    await state.clear()
    await state.set_state(OnSetDailyAllow.gender_waiting)
    await message.answer(f"Приятно познакомиться, {user_name}! Ответь на пару легких вопросов")
    await log_message_id(state, message.message_id)
    await message.answer(
        "Укажите ваш пол.",
        reply_markup=get_inline_gender_answer()
    )
    await log_message_id(state, message.message_id)

@router.callback_query(lambda c: c.data == "btn_man")
async def process_callback_man(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    await state.update_data(user_gender="Man")
    
    await callback_query.message.edit_text(
        text="Отлично! Какой твой вес? Напиши числом"
    )
    await log_message_id(state, callback_query.message.message_id)

    await state.set_state(OnSetDailyAllow.weight_waiting)

@router.callback_query(lambda c: c.data == "btn_girl")
async def process_callback_man(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    await state.update_data(user_gender="Girl")
    
    await callback_query.message.edit_text(
        text="Отлично! Какой твой вес? Напиши числом"
    )
    await log_message_id(state, callback_query.message.message_id)

    await state.set_state(OnSetDailyAllow.weight_waiting)

@router.message(OnSetDailyAllow.weight_waiting, F.text)
async def weight_waiting(message: types.Message, state: FSMContext):
    await log_message_id(state, message.message_id)

    user_weight = message.text

    if user_weight.isdigit():
        await state.update_data(user_weight=user_weight)
        await state.set_state(OnSetDailyAllow.height_waiting)
        await message.answer("Последний шаг. Напиши свой рост числом")
        await log_message_id(state, message.message_id)
    else:
        await message.delete()

@router.message(OnSetDailyAllow.height_waiting, F.text)
async def height_waiting(message: types.Message, state: FSMContext, db, bot, ai):
    await log_message_id(state, message.message_id)
    
    user_height = message.text

    if user_height.isdigit():
        await state.update_data(user_height=user_height)
        await message.answer("Считаю...")
        await log_message_id(state, message.message_id)
        await allow_waiting(message, state, db, bot, ai)
    else:
        await message.delete()

async def allow_waiting(message: types.Message, state: FSMContext, db, bot, ai):
    id = message.from_user.id

    user_data = await state.get_data()
    gender = user_data.get("user_gender")
    weight = user_data.get("user_weight") 
    height = {user_data.get("user_height")}

    all_data_prompt = f"Gender: {gender}, Weight: {weight}kg, Height: {height}cm"

    await delete_log_message(state, message, bot, user_data)

    try:
        allow = await GetDayAllow(all_data_prompt, id, db, ai)

        await state.clear()
        await message.answer(f"""Отлично! Твоя дневная норма: {allow} каллорий🥕
        Начнем считать твой рацион. Напиши что ты съел(а) за сегодня.""")
    except:
        logger.info("Get error in buisness request")
        await message.answer("Извини, в данный момент не могу обработать запрос... Но разработчик сейчас работает над этим. Попробуй позже")

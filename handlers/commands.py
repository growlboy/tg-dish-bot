from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode

from services.data_process import GetTodayCal, GetDayAllow
from display.error_messages import default_error

router = Router()

@router.message(Command("tc"))
async def cmd_todaycheck(message: types.Message, db):
    tg_id = message.from_user.id
    answer = await GetTodayCal(tg_id, db)
    allow = await GetDayAllow(tg_id, db)

    if allow:
        result_string = "Суточная норма не превышена. Ешь на здоровье!✅"

        if allow < answer:
            result_string = "Немного превышена суточная норма 🤔"

        text = (
        f"Всего на сегодня: {answer} / {allow} каллорий\n\n"
        f"{result_string}"
        )
        
        await message.answer(text=text, parse_mode=ParseMode.HTML)
    else:
        await default_error(message)

@router.message(Command("ac"))
async def cmd_todaycheck(message: types.Message, db):
    tg_id = message.from_user.id
    answer = await GetDayAllow(tg_id, db)

    if answer:
        await message.answer(f"""Ваша суточная норма: {answer} каллорий 🥕""")
    else:
        await default_error(message)

@router.message(Command("history"))
async def cmd_todaycheck(message: types.Message, db):
    await message.answer("Пока не сделал😦")
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("todaycheck"))
async def cmd_todaycheck(message: types.Message, db):
    tg_id = message.from_user.id
    answer = await db.GetTodayCal(tg_id)

    if answer:
        await message.answer(f"""Всего на сегодня: {str(answer)} каллорий ✅""")
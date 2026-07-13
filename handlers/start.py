from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import OnRegistration

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext, db):
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
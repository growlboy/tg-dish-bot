from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
import logging

from services.data_process import PlusCallories, IsRegister

logger = logging.getLogger(__name__)

router = Router()

@router.message(F.text)
async def prompt_reading(message: types.Message, db, ai):
    try:
        tg_id = message.from_user.id
        prompt = message.text

        if await IsRegister():
            answer = await PlusCallories(prompt, tg_id, db, ai)

            if answer[0] and answer[1]:
                await message.answer(f"""Это вышло на {answer[0]} каллорий.
                Всего на сегодня: {answer[1]} каллорий ✅""")
        
        else:
            await message.answer("Вы еще не зарегистрированы...")

    except:
        logger.info("Get error in buisness request")
        await message.answer("Извини, в данный момент не могу обработать запрос... Но разработчик сейчас работает над этим. Попробуй позже")
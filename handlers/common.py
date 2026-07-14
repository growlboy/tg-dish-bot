from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
import logging
from aiogram.enums import ParseMode

from services.data_process import PlusCallories, IsRegister, GetDayAllow
from display.error_messages import default_error

logger = logging.getLogger(__name__)

router = Router()

@router.message(F.text)
async def prompt_reading(message: types.Message, db, ai):
    try:
        tg_id = message.from_user.id
        prompt = message.text

        if await IsRegister(tg_id, db):
            answer = await PlusCallories(prompt, tg_id, db, ai)
            today_allow = await GetDayAllow(tg_id, db)
            
            result_string = "Суточная норма не превышена. Ешь на здоровье!✅"

            if int(today_allow) > int(answer[1]):
                result_string = "Немного превышена суточная норма 🤔"

            text = (
            f"Это вышло на {answer[0]} каллорий.🥕 \n\n"
            f"Всего на сегодня: {answer[1]} / {today_allow} каллорий \n\n"
            f"{result_string}"
            )

            if answer[0] and answer[1] and today_allow:
                await message.answer(text=text, parse_mode=ParseMode.HTML)
            else:
                await default_error(message)
        
        else:
            await message.answer("Вы еще не зарегистрированы...")

    except Exception as error:
        print(error)
        logger.info("Get error in buisness request")
        await default_error(message)
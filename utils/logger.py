from aiogram.fsm.context import FSMContext
from aiogram import types
import logging

logger = logging.getLogger(__name__)

async def log_message_id(state: FSMContext, message_id: int):
    data = await state.get_data()

    msg_ids = data.get("messages_to_delete", [])
    msg_ids.append(message_id)

    await state.update_data(messages_to_delete=msg_ids)

async def delete_log_message(state: FSMContext, message: types.Message, bot, user_data):
    msg_ids_to_delete = user_data.get("messages_to_delete", [])

    try:
        await bot.delete_messages(
            chat_id=message.chat.id, 
            message_ids=msg_ids_to_delete
        )
    except Exception as error:
        logger.info("Error with delete cash.")
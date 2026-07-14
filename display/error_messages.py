from aiogram import types

async def default_error(message: types.Message):
    await message.answer("Извини, в данный момент не могу обработать запрос... Но разработчик сейчас работает над этим. Попробуй позже")

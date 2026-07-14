from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_inline_gender_answer():
    girl = InlineKeyboardButton(text="Девушка🚺", callback_data="btn_girl")
    man = InlineKeyboardButton(text="Парень🚹", callback_data="btn_man")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[girl, man]])
    return keyboard
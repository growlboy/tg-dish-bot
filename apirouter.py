import os
import aiohttp
import json 

PROMPT = """(Пиши на русском, пожалуйста. Я пишу блюдо, ты списком разделяешь его на состовляющие магазинные продукты. 
            Пиши только продукты через перенос на новую строку и можешь в конце каждого продукта символично указывать насколько оно важно в блюде символом ★ (от 1 до 4).
            Если такого блюда не существует или оно слишком сумбурное для реальности пиши "Извините, но это врятли похоже на блюдо, возможно вы имели...")"""

async def datarequest(dish):
    fullprompt = PROMPT + dish

    url=os.getenv("OPEN_ROUTER_API")
    headers={
        "Authorization": os.getenv("AUTH_TOKEN")
    }
    data={
        "model": os.getenv("MODEL"),
        "messages":[
            {
            "role": "user",
            "content": fullprompt
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                response_data = await response.json()
                text_message = response_data['choices'][0]['message']['content']

                return text_message
            else:
                return "Прости.. Пока службы не работают"
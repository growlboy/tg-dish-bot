import os
import aiohttp
import json 

PROMPT = """Проанализируй предложенную строку и выдай в ответе только ОДНО число без ислючений - примерное количество калорий
            в продуктах написанных в строке."""

API_KEY = os.getenv("AUTH_TOKEN")
URL = os.getenv("OPEN_ROUTER_API")
    
headers = {
    "Authorization": API_KEY,
}

async def datarequest(prompt):
    data = f"""Проанализируй предложенную строку {prompt} и выдай в ответе только ОДНО число без ислючений - примерное количество калорий
            в продуктах написанных в строке."""

    payload = {
        "model": os.getenv("MODEL"),
        "messages": [
            {"role": "user", "content": data}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(URL, headers=headers, json=payload) as response:
            print(response.status)
            if response.status == 200:
                response_data = await response.json()
                text_message = response_data['choices'][0]['message']['content']
                
                return text_message
            else:
                return "None"
            

async def dayallowrequest(prompt):
    data = f"""Проанализируй предложенную строку {prompt} и по параметрам выдай в ответе только ОДНО число без ислючений - примерную норму
                каллорий для человека для поддержания стройной фигуры"""
    
    payload = {
        "model": os.getenv("MODEL"),
        "messages": [
            {"role": "user", "content": data}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(URL, headers=headers, json=payload) as response:
            print(response.status)
            if response.status == 200:
                response_data = await response.json()
                text_message = response_data['choices'][0]['message']['content']
                
                return text_message
            else:
                return "None"
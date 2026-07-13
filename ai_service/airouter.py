import aiohttp
from config import *
import logging

logger = logging.getLogger(__name__)

async def request(payload):
    headers = {
        "Authorization": MODEL_API_KEY,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(MODEL_URL, headers=headers, json=payload) as response:
                print(response.status)
                if response.status == 200:
                    response_data = await response.json()
                    text_message = response_data['choices'][0]['message']['content']
                
                    return text_message, 200
                else:
                    return None, response.status
    except:
        logger.exception()
        logger.info("Error in request")
        return None, 400

class AiRouterConnect:
    async def count_callories_request(self, prompt):
        data = f"""Проанализируй предложенную строку {prompt} и выдай в ответе только ОДНО число без ислючений - примерное количество калорий
        в продуктах написанных в строке."""

        payload = {
            "model": MODEL_V,
            "messages": [
                {"role": "user", "content": data}
            ]
        }

        return request(payload)
                

    async def day_allow_request(self, prompt):
        try:
            data = f"""Проанализируй предложенную строку {prompt} и по параметрам выдай в ответе только ОДНО число без ислючений - примерную норму
            каллорий для человека для поддержания стройной фигуры"""

            payload = {
                "model": MODEL_V,
                "messages": [
                    {"role": "user", "content": data}
                ]
            }   

            return request(payload)
        except Exception as error:
            print(error)

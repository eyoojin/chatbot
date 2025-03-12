import os
import requests
import random
from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI, Request

from utils import kospi

app = FastAPI()

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'


@app.post("/") # get: 데이터를 줘 # post: 데이터를 줄테니까 처리해줘
async def read_root(request: Request): # async: 비동기적 함수
    body = await request.json() # await: 데이터가 처리될 때까지 기다려
    
    user_id = body['message']['chat']['id']
    text = body['message']['text']

    if text[0] == '/': # 키워드로 대답
        if text == '/lotto':
            numbers = random.sample(range(1, 46), 6)
            output = str(sorted(numbers))
        elif text == '/kospi':
            output = kospi()
        else:
            output = 'X'

    else: # 모든 대답
        output = '지원하지 않는 기능입니다.'

    requests.get(f'{URL}/sendMessage?chat_id={user_id}&text={output}')

    return body

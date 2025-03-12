import os
import requests
import random
from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI, Request

from utils import kospi, openai, langchain

app = FastAPI()

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
URL = f'https://api.telegram.org/bot{TOKEN}'


@app.post("/") # get: 데이터를 줘 # post: 데이터를 줄테니까 처리해줘
async def read_root(request: Request): # async: 비동기적 함수
    body = await request.json() # await: 데이터가 처리될 때까지 기다려
    
    user_id = body['message']['chat']['id']
    text = body['message']['text']

    if text[0] == '/': # 키워드로 대답
        if text == '/lotto':
            numbers = random.sample(range(1, 46), 6)
            output = '로또 번호를 추천해드릴게요.\n' + str(sorted(numbers)) + ' 어때요?\n행운을 빌어요!'
        elif text == '/kospi':
            output = '현재 코스피는 ' + kospi() + '입니다.'
        elif text == '/menu':
            menu = random.choice(['한식', '중식', '일식', '양식', '분식'])
            if menu == '한식':
                korean = random.choice(['김치찌개', '제육볶음', '된장찌개', '순대국밥'])
                output = '오늘은 ' + str(menu) + '의 ' + str(korean) + '을(를) 먹어보세요!'

            else:
                output = '오늘은 ' + str(menu) + '을 먹어보세요!'
        else:
            output = '지원하지 않는 키워드예요!'

    else: # 모든 대답
        output = langchain(text)

    requests.get(f'{URL}/sendMessage?chat_id={user_id}&text={output}')

    return body

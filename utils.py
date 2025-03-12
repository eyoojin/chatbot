import requests
from bs4 import BeautifulSoup

def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/'
    res = requests.get(KOSPI_URL) # html 정보
    
    selector = '#KOSPI_now'
    soup = BeautifulSoup(res.text, 'html.parser')
    kospi = soup.select_one(selector)

    return kospi.text

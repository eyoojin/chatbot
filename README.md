- `python -m venv venv`
- `source venv/Scripts/activate`
- `pip install python-dotenv`
- `pip install requests`
- `pip install fastapi`
- `pip install "uvicorn[standard]"`
- `pip install beautifulsoup4`
- `pip install openai`

- [LangChain](https://python.langchain.com/docs/tutorials/rag/)
    - OpenAI -> OpenAI -> In-memory

---

- 터미널1: fastapi
    - `source venv/Scripts/activate`
    - `uvicorn main:app --reload`

- 터미널2: ngrok
    - `./ngrok.exe http 8000` -> 링크를 `.env`에 저장

- 터미널3:
    - `source venv/Scripts/activate`
    - `python 01_webhook.py`
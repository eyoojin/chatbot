import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/'
    res = requests.get(KOSPI_URL) # html 정보

    selector = '#KOSPI_now'
    soup = BeautifulSoup(res.text, 'html.parser')
    kospi = soup.select_one(selector)

    return kospi.text

def openai(api_key, user_input):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model='gpt-4o',
        messages=[ # role: system, user, AI
            {'role': 'system', 'content': '당신은 사용자와 대화하는 챗봇입니다. 친근하게 대답해주세요.'}, 
            {'role': 'user', 'content': user_input},
        ]
    )
    
    return completion.choices[0].message.content

def langchain(user_input):
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large") # 글자 데이터를 숫자 데이터로 변경
    vector_store = InMemoryVectorStore(embeddings)

    # 1. load document
    loader = WebBaseLoader(
        web_paths=(
            'https://www.edaily.co.kr/news/read?newsId=01292326638851856&mediaCodeNo=258',
        )
    )
    docs = loader.load()

    # 2. split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    all_splits = text_splitter.split_documents(docs)

    # 3. store
    _ = vector_store.add_documents(documents=all_splits) # _: 안 쓰이는 변수, 저장하는 데 의미

    # 4. retrieve
    prompt = hub.pull('rlm/rag-prompt')
    retrieved_docs = vector_store.similarity_search(user_input) # 유사도 검색
    docs_content = '\n\n'.join(doc.page_content for doc in retrieved_docs)
    prompt = prompt.invoke({'question': user_input, 'context': docs_content}) # invoke: 불러오다, 질문하는 느낌
    answer = llm.invoke(prompt).content
    
    return answer
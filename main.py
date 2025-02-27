from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import requests
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
import dairy_model
import threading


# 환경 변수 로드
load_dotenv()

# LangChain GPT-4o 모델 초기화
model = init_chat_model("gpt-4o", model_provider="openai")

# FastAPI 앱 생성
app = FastAPI()

main_model = dairy_model.DIARY()

class DiaryRequest(BaseModel):
    tone: str
    mood: str
    wakeTime: str
    food: List[str]
    userDo: List[str]
    meetPeople: List[str]
    extSentence: str

@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

@app.post("/generate_diary")
async def generate_diary_entry(data: DiaryRequest):
    def on_server_start(data):
        # 서버가 열린 후 특정 API 요청을 자동으로 실행 가능
        url = "http://13.124.98.245:8000/generate_diary"
        response = requests.post(url, json=data)


    # 서버가 시작될 때 자동 실행되는 이벤트
    @app.on_event("startup")
    def startup_event():
        threading.Thread(target=on_server_start, daemon=True).start()

    #print("out_input", data)

    diary_kor, diary_eng, diary_Japan, diary_China, diary_latin, diary_summary = main_model.generate_diary(data) # AI가 일기 작성

    return {"diary_kor": diary_kor.content,
        "diary_eng" : diary_eng.content,
        "diary_japan" : diary_Japan.content, 
        "diary_China" : diary_China.content, 
        "diary_latin" : diary_latin.content,
        "summary" : diary_summary.content}
    
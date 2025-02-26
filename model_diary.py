from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import requests
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage


# 환경 변수 로드
load_dotenv()

# LangChain GPT-4o 모델 초기화
model = init_chat_model("gpt-4o", model_provider="openai")

# FastAPI 앱 생성
app = FastAPI()

def load_json(url):
    response = requests.get(url)
    json_data = response.json()
    return json_data

# JSON 데이터 모델 정의
class DIARY:
    def __init__(self):
        load_dotenv()
        self.url = "https://effective-journey-4jgjwgvgqqgg3jwjw-8000.app.github.dev/get_data" #사이트 주소 넣어주세요!
        self.input_data = {
            "tone":"princess",
            "condition":"good",
            "wakeTime":"09:00:00",
            "food":["밥", "김치", "미역국"],
            "userDo":["운동", "공부", "술"],
            "meetPeople":["그레이", "비키"],
            "extSentence":"오늘 하루 힘내자"
        }#load_json(self.url)
        self.model = init_chat_model("gpt-4o-mini", model_provider = "openai")
        self.prompt_template = f"""
            당신은 사용자 맞춤형 AI 일기 작성 도우미입니다.
            아래 정보를 바탕으로 사용자에게 친근하게 하루 일기를 작성해주세요.

            - 톤: {self.input_data['tone']}
            - 컨디션: {self.input_data['condition']}
            - 기상 시간: {self.input_data['wakeTime']}
            - 먹은 음식: {', '.join(self.input_data['food'])}
            - 한 일: {', '.join(self.input_data['userDo'])}
            - 만난 사람: {', '.join(self.input_data['meetPeople'])}
            - 추가 문장: "{self.input_data['extSentence']}"

            위 내용을 바탕으로 톤에 충실한 이모티콘을 사용하여 자연스럽고 감성적인 일기를 작성해주세요.
            """
    # JSON 파일 로드 함수
    
    def translate(self, language, response_kor):
        translate_prompt = f"""당신은 {language}와 영어에 원어민 수준의 유창성을 갖춘 전문 번역가입니다.  
                    당신의 역할은 주어진 원문을 {language}로 번역하는 것입니다.
                    이 과정에서 의미, 어조, 문맥을 가능한 정확하게 유지해야 합니다.

                    **원문:** {response_kor}  
                    **정확한 번역:**
                    """
        return translate_prompt

    #이 과정에서 의미, 어조, 문맥을 100% 정확하게 유지해야 합니다.
    # 일기 생성
    def generate_diary(self, data):
        response_kor = model.invoke(self.prompt_template)
        response_eng = model.invoke(self.translate("English", response_kor))
        response_Japan = model.invoke(self.translate("Japanese", response_kor))
        response_China = model.invoke(self.translate("Chinese", response_kor))
        reponse_latin = model.invoke(self.translate("Latina", response_kor))
        return response_kor, response_eng, response_Japan, response_China, reponse_latin

main_model = DIARY()

@app.get("/generate_diary")
async def generate_diary_entry():

    data = {
        "tone":"princess",
        "condition":"good",
        "wakeTime":"09:00:00",
        "food":["밥", "김치", "미역국"],
        "userDo":["운동", "공부", "술"],
        "meetPeople":["그레이", "비키"],
        "extSentence":"오늘 하루 힘내자"
    } # JSON 데이터 불러오기
    diary_kor, diary_eng, diary_Japan, diary_China, diary_latin = main_model.generate_diary(data)  # AI가 일기 작성
    print(diary_kor.content, diary_eng.content)
    return {"diary_kor": diary_kor.content, 
            "diary_eng" : diary_eng.content, 
            "diary_japan" : diary_Japan, 
            "diary_China" : diary_China, 
            "diary_latin" : diary_latin}

if __name__ == '__main__':
    url = "https://effective-journey-4jgjwgvgqqgg3jwjw-8000.app.github.dev/get_data"
    data = load_json(url)
    print(data)
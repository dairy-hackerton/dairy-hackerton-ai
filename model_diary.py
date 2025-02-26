from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

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
        self.input_data = None
        self.url = "" #사이트 주소 넣어주세요!
        self.model = init_chat_model("gpt-4o-mini", model_provider = "openai")
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""
                    당신은 사용자 맞춤형 AI 일기 작성 도우미입니다.
                    아래 정보를 바탕으로 사용자에게 친근하게 하루 일기를 작성해주세요.

                    - 톤: {input_data['tone']}
                    - 컨디션: {input_data['condition']}
                    - 기상 시간: {input_data['wakeTime']}
                    - 먹은 음식: {', '.join(input_data['food'])}
                    - 한 일: {', '.join(input_data['userDo'])}
                    - 만난 사람: {', '.join(input_data['meetPeople'])}
                    - 추가 문장: "{input_data['extSentence']}"

                    위 내용을 바탕으로 톤에 충실한 이모티콘을 사용하여 자연스럽고 감성적인 일기를 작성해주세요.
                    """,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        self.translate_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""당신은 {language}와 영어에 원어민 수준의 유창성을 갖춘 전문 번역가입니다.  
                    당신의 역할은 주어진 원문을 {language}로 번역하는 것입니다.  
                    이 과정에서 의미, 어조, 문맥을 100% 정확하게 유지해야 합니다.

                    **원문:** {text}  
                    **정확한 번역:**
                    """
                )
            ]
        )
    # JSON 파일 로드 함수
    
    def translate(language, response_kor):
        translate_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""당신은 {language}와 영어에 원어민 수준의 유창성을 갖춘 전문 번역가입니다.  
                    당신의 역할은 주어진 원문을 {language}로 번역하는 것입니다.  
                    이 과정에서 의미, 어조, 문맥을 100% 정확하게 유지해야 합니다.

                    **원문:** {response_kor}  
                    **정확한 번역:**
                    """
                )
            ]
        )
        return translate_prompt

    # 일기 생성
    def generate_diary(data):
        response_kor = model.invoke(self.prompt_template)
        response_eng = model.invoke(translate("English", response_kor))
        response_Japan = model.invoke(translate("Japanese", response_kor))
        response_China = model.invoke(translate("Chinese", response_kor))
        reponse_latin = model.invoke(translate("Latina", response_kor))
        return response

@app.get("/generate_diary")
async def generate_diary_entry():
    data = load_json()  # JSON 데이터 불러오기
    diary_entry = generate_diary(data)  # AI가 일기 작성
    return {"diary": diary_entry.content}
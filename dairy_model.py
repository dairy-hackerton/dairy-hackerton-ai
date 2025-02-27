from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import requests
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

class DiaryRequest(BaseModel):
    tone: str
    mood: str
    wakeTime: str
    food: List[str]
    userDo: List[str]
    meetPeople: List[str]
    extSentence: str

# JSON 데이터 모델 정의
class DIARY:
    def __init__(self):
        load_dotenv()
        self.tone = ""
        self.model = init_chat_model("gpt-4o-mini", model_provider = "openai")
        self.prompt_template = ""
    # JSON 파일 로드 함수

    def diary_prompt(self, data):
        self.prompt_template = f"""
            당신은 사용자 맞춤형 AI 일기 작성 도우미입니다.
            아래 정보를 바탕으로 사용자에게 친근하게 하루 일기를 작성해주세요.

            - 톤: {self.tone}
            - 컨디션: {data.mood}
            - 기상 시간: {data.wakeTime}
            - 먹은 음식: {', '.join(data.food)}
            - 한 일: {', '.join(data.userDo)}
            - 만난 사람: {', '.join(data.meetPeople)}
            - 추가 문장: "{data.extSentence}"

            위 내용을 바탕으로 톤에 충실한 이모티콘을 사용하여 톤과 컨디션에 가까운 느낌으로 10문장 이내의 일기를 작성해주세요.
            꼭 한국말로 생성해주되, 날짜 빼줘.
            """

    def summary(self, response_kor):
        summary_prompt = f"""아래 문장을 핵심 의미만 남기고 10자 이내로 자연스럽게 요약해줘.
        문장의 의미를 유지하면서도 가능한 짧고 간결하게 표현해야 해.  
        불필요한 단어는 제거하고, 핵심 단어 위주로 구성해줘.  
        재미있게 요약해주되, 요약한 문장만 도출해줘.

        문장: "{response_kor}"  
        요약된 문장:"""
        return summary_prompt

    def change_tone(self):
        if self.tone == "MZ 세대":
            self.tone = "2025 기준 밈을 사용한 MZ세대 경박하고 어미엔 음,슴체를 쓰는 말투"
        
        elif self.tone == "사극":
            self.tone = "사극 말투를 사용하는 근엄한 조선시대 왕 말투"

        elif self.tone == "데일리": 
            self.itone = "general"

        elif self.tone == "사춘기 중학생":
            self.tone = "상처받을 정도로 시비거는 말투"

        elif self.tone == "공주": 
            self.tone = "princess"
        
        else:    
            pass
    

    def translate(self, language, response_kor):
        translate_prompt = f"""당신은 {language}와 영어에 원어민 수준의 유창성을 갖춘 전문 번역가입니다.  
                    당신의 역할은 주어진 원문을 {language}로 번역하는 것입니다.
                    이 과정에서 의미, 어조, 문맥을 가능한 정확하게 반영해야 합니다.
                    반드시 번역한 내용을 도출해야 하며, 번역한 내용만 도출하세요.

                    **원문:** {response_kor}  
                    **정확한 번역:**
                    """
        return translate_prompt

    # 일기 생성
    def generate_diary(self, data: DiaryRequest):
        self.tone = data.tone
        self.change_tone()
        
        self.diary_prompt(data) #다이어리 프롬프트 지정.(input은 body)

        response_kor = self.model.invoke(self.prompt_template)
        response_eng = self.model.invoke(self.translate("English", response_kor))
        response_Japan = self.model.invoke(self.translate("Japanese", response_kor))
        response_China = self.model.invoke(self.translate("Chinese", response_kor))
        reponse_latin = self.model.invoke(self.translate("Latina", response_kor))
        reponse_summary = self.model.invoke(self.summary(response_kor))
        return response_kor, response_eng, response_Japan, response_China, reponse_latin, reponse_summary
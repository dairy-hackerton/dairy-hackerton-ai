from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# JSON 데이터 모델 정의
class DataModel(BaseModel):
    tone: str
    condition: str
    wakeTime: str
    food: List[str]
    userDo: List[str]
    meetPeople: List[str]
    extSentence: str

# 제공할 JSON 데이터
data = DataModel(
    tone="princess",
    condition="good",
    wakeTime="09:00:00",
    food=["밥", "김치", "미역국"],
    userDo=["운동", "공부", "술"],
    meetPeople=["그레이", "비키"],
    extSentence="오늘 하루 힘내자"
)

@app.get("/get_data", response_model=DataModel)
async def get_data():
    return data

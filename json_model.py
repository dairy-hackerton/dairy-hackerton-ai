from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json

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

# JSON 파일 로드
def load_json():
    with open("dummy.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.get("/get_data", response_model=DataModel)
async def get_data():
    data = load_json()
    print(data)
    return data
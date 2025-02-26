from dotenv import load_dotenv
from request

#lanbchain모듈 불러오기
from langchain.chat_models import init_chat_model


#일기 모델
class DIARY:
    def __init__(self, dummy_data):
        load_dotenv()
        self.model = init_chat_model("gpt-4o-mini", model_provider = "openai")
        url = "https://orange-chainsaw-q7qgpx95p9gxc6wr9-8000.app.github.dev/get_data"
        response = requests.get(url)
        json_data = response.json()
        self.dummy = dummy_data
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"You are a {self.dummy["tone"]}. Answer all questions to the best of your ability in Korean.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

    def get_reponse(self, message):
        return self.model.invoke([HumanMessage(message)])
    
    def get_prompt_reponse(self, message):
        prompt = self.prompt_template.invoke({"language": "Korean", "text" : message})
        return self.model.invoke(prompt)
    
    def get_streaming_response(self, messages):
        return self.model.astream(messages)
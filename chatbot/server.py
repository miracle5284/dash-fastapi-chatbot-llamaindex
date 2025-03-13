from fastapi import FastAPI
from .indexing import get_faq_index
from .schemas import Query
from .chatbot import send_prompt_to_openai
from pydantic import BaseModel
from fastapi import HTTPException


index = get_faq_index()
engine = index.as_query_engine()
app = FastAPI()

@app.post('/')
async def index(request: Query):
    result = engine.query(request.question)
    return result

class Message(BaseModel):
    role: str
    content: str

class PromptRequest(BaseModel):
    messages: list[Message]

@app.post("/generate-response/")
async def generate_response(request: PromptRequest):
    try:
        print('1111111111111\n', request.messages)
        response = send_prompt_to_openai(request.messages)
        return {"response": response}
    except ImportError as e:
        raise HTTPException(status_code=500, detail=str(e))

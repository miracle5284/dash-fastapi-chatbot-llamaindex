from pydantic import BaseModel


class Query(BaseModel):
    question: str
    

class Message(BaseModel):
    role: str
    content: str


class PromptRequest(BaseModel):
    messages: list[Message]

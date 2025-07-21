from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Query(BaseModel):
    question: str
    

class Message(BaseModel):
    role: str
    content: str


class PromptRequest(BaseModel):
    messages: list[Message]


# Authentication schemas
class UserCreate(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Chat and Message schemas
class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True


class ChatListResponse(BaseModel):
    chats: List[ChatResponse]


# AI Response schemas
class AIResponseRequest(BaseModel):
    chat_id: Optional[int] = None
    user_question: str
    return_with_history: bool = False


class AIResponseResponse(BaseModel):
    response: str
    chat_id: int
    messages: Optional[List[MessageResponse]] = None

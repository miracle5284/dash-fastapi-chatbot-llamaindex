from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import os

from .indexing import get_faq_index
from .schemas import (
    Query, Message, PromptRequest, UserCreate, UserLogin, Token, 
    UserResponse, ChatResponse, ChatListResponse, AIResponseRequest, AIResponseResponse,
    SystemPromptResponse, SystemPromptUpdate
)
from .chatbot import send_prompt_to_openai
from .database import get_db, create_tables, check_database_schema
from .models import User, Chat, Message as MessageModel
from .auth import (
    get_password_hash, verify_password, create_access_token, 
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from .prompt_manager import prompt_manager
from .admin_setup import create_default_admin

# Initialize FastAPI app
app = FastAPI(title="Chatbot API", version="1.0.0")

# Initialize FAQ index
# index = get_faq_index()
# engine = index.as_query_engine()

# Create database tables and default admin on startup
@app.on_event("startup")
async def startup_event():
    # Check if database schema needs migration
    schema_updated = check_database_schema()
    
    # Only create tables if they don't exist or were recreated
    if schema_updated:
        print("🔄 Tables were recreated, creating admin user...")
    else:
        # Tables exist and are up to date, just ensure they exist
        create_tables()
        print("✅ Database tables are ready.")
    
    # Always try to create admin user
    create_default_admin()

# Helper function to check if user is admin
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.user_type != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Authentication endpoints
@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user (always as student)
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        user_type="student",  # Always create as student
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# System Prompt Management (Admin Only)
@app.get("/system-prompt", response_model=SystemPromptResponse)
async def get_system_prompt(current_user: User = Depends(require_admin)):
    """Get the current system prompt (Admin only)"""
    prompt = prompt_manager.get_prompt()
    return SystemPromptResponse(prompt=prompt)

@app.put("/system-prompt", response_model=SystemPromptResponse)
async def update_system_prompt(
    prompt_update: SystemPromptUpdate,
    current_user: User = Depends(require_admin)
):
    """Update the system prompt (Admin only)"""
    success = prompt_manager.set_prompt(prompt_update.prompt)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update system prompt"
        )
    
    return SystemPromptResponse(prompt=prompt_update.prompt)

# Chat management endpoints
@app.get("/chats", response_model=ChatListResponse)
async def get_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all chats for the current user"""
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).all()
    return ChatListResponse(chats=chats)

@app.get("/chats/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific chat with all its messages"""
    chat = db.query(Chat).filter(
        Chat.id == chat_id, 
        Chat.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    return chat

# AI Response endpoint
@app.post("/get_ai_response", response_model=AIResponseResponse)
async def get_ai_response(
    request: AIResponseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI response for a user question, optionally creating a new chat or using existing one"""
    
    # Get system prompt dynamically
    system_prompt = prompt_manager.get_prompt()
    
    messages = []
    
    if request.chat_id is None:
        # Create new chat
        chat = Chat(user_id=current_user.id, title=request.user_question[:50] + "...")
        db.add(chat)
        db.commit()
        db.refresh(chat)
        
        # Add system message to new chat
        system_message = MessageModel(
            chat_id=chat.id,
            role="system",
            content=system_prompt
        )
        db.add(system_message)
        db.commit()
        
        chat_id = chat.id
        # Add system message to messages list for OpenAI
        messages.append({"role": "system", "content": system_prompt})
    else:
        # Get existing chat
        chat = db.query(Chat).filter(
            Chat.id == request.chat_id,
            Chat.user_id == current_user.id
        ).first()
        
        if not chat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found"
            )
        
        chat_id = request.chat_id
        # Get existing messages for this chat
        existing_messages = db.query(MessageModel).filter(
            MessageModel.chat_id == chat_id
        ).order_by(MessageModel.created_at).all()
        
        # Convert to format expected by OpenAI
        for msg in existing_messages:
            messages.append({"role": msg.role, "content": msg.content})
    
    # Add user's new question
    user_message = MessageModel(
        chat_id=chat_id,
        role="user",
        content=request.user_question
    )
    db.add(user_message)
    db.commit()
    
    # Add user message to messages list for OpenAI
    messages.append({"role": "user", "content": request.user_question})
    
    # Get AI response
    try:
        ai_response_text = send_prompt_to_openai(messages)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting AI response: {str(e)}"
        )
    
    # Save AI response to database
    ai_message = MessageModel(
        chat_id=chat_id,
        role="assistant",
        content=ai_response_text
    )
    db.add(ai_message)
    db.commit()
    
    # Update chat's updated_at timestamp
    chat.updated_at = db.query(Chat).filter(Chat.id == chat_id).first().updated_at
    db.commit()
    
    # Prepare response
    response_data = {
        "response": ai_response_text,
        "chat_id": chat_id,
        "messages": None
    }
    
    if request.return_with_history:
        # Get all messages for this chat, newest first
        all_messages = db.query(MessageModel).filter(
            MessageModel.chat_id == chat_id
        ).order_by(MessageModel.created_at.desc()).all()
        
        response_data["messages"] = all_messages
    
    return AIResponseResponse(**response_data)

# Legacy endpoints (keeping for backward compatibility)
# @app.post('/')
# async def index(request: Query):
#     result = engine.query(request.question)
#     return result

@app.post("/generate-response/")
async def generate_response(request: PromptRequest):
    try:
        response = send_prompt_to_openai(request.messages)
        return {"response": response}
    except ImportError as e:
        raise HTTPException(status_code=500, detail=str(e))

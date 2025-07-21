# Chatbot API Documentation

## Overview

This API provides a complete chatbot system with user authentication, chat history management, and AI-powered responses. The system uses JWT authentication, SQLite database, and integrates with OpenAI for AI responses.

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. All protected endpoints require a Bearer token in the Authorization header.

### Register User
- **POST** `/register`
- **Body:**
```json
{
    "username": "string",
    "email": "string",
    "first_name": "string",  // optional
    "last_name": "string",   // optional
    "password": "string"
}
```
- **Response:** User information (without password)

### Login
- **POST** `/login`
- **Body:**
```json
{
    "username": "string",
    "password": "string"
}
```
- **Response:**
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

### Get Current User Info
- **GET** `/me`
- **Headers:** `Authorization: Bearer <token>`
- **Response:** Current user information

## Chat Management

### Get All Chats
- **GET** `/chats`
- **Headers:** `Authorization: Bearer <token>`
- **Response:**
```json
{
    "chats": [
        {
            "id": 1,
            "title": "string",
            "created_at": "datetime",
            "updated_at": "datetime",
            "messages": [...]
        }
    ]
}
```

### Get Specific Chat
- **GET** `/chats/{chat_id}`
- **Headers:** `Authorization: Bearer <token>`
- **Response:** Chat with all messages

## AI Response

### Get AI Response
- **POST** `/get_ai_response`
- **Headers:** `Authorization: Bearer <token>`
- **Body:**
```json
{
    "chat_id": null,  // null for new chat, or existing chat ID
    "user_question": "string",
    "return_with_history": false  // true to return all messages
}
```
- **Response:**
```json
{
    "response": "AI response text",
    "chat_id": 1,
    "messages": null  // or array of messages if return_with_history=true
}
```

## API Behavior

### Creating New Chats
- When `chat_id` is `null`, a new chat is created
- The system prompt is automatically added as the first message
- The user's question becomes the chat title (truncated to 50 characters)

### Continuing Existing Chats
- When `chat_id` is provided, the system fetches the chat history
- All previous messages are included in the context sent to OpenAI
- The conversation maintains context across multiple exchanges

### Message History
- When `return_with_history=true`, all messages are returned sorted newest to oldest
- When `return_with_history=false`, only the AI response is returned
- Messages include role (user/assistant/system), content, and timestamp

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `first_name`: User's first name (optional)
- `last_name`: User's last name (optional)
- `hashed_password`: Bcrypt hashed password
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

### Chats Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `title`: Chat title
- `created_at`, `updated_at`: Timestamps

### Messages Table
- `id`: Primary key
- `chat_id`: Foreign key to chats
- `role`: Message role (user/assistant/system)
- `content`: Message content
- `created_at`: Timestamp

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (validation errors)
- `401`: Unauthorized (invalid token)
- `404`: Not found (chat not found)
- `500`: Internal server error

## Security Features

1. **Password Hashing**: Uses bcrypt for secure password storage
2. **JWT Tokens**: Secure token-based authentication
3. **User Isolation**: Users can only access their own chats
4. **Input Validation**: All inputs are validated using Pydantic models

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_MODEL_NAME="gpt-3.5-turbo"  # optional
```

3. Run the server:
```bash
python -m uvicorn chatbot.server:app --reload
```

4. Test the API:
```bash
python test_api.py
```

## Legacy Endpoints

The following endpoints are maintained for backward compatibility:
- `POST /` - FAQ query endpoint
- `POST /generate-response/` - Legacy AI response endpoint

## Notes

- The database file (`chatbot.db`) is created automatically on first run
- JWT tokens expire after 30 minutes
- The system prompt is read from `system_prompt.txt` file
- All timestamps are in UTC 
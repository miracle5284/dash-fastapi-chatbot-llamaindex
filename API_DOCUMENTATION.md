# Chatbot API Documentation

## Overview

This API provides a complete chatbot system with user authentication, chat history management, and AI-powered responses. The system uses JWT authentication, SQLite database, and integrates with OpenAI for AI responses. It supports two user types: **admin** and **student**.

## User Types

- **Admin**: Can access all features including system prompt management
- **Student**: Can use chat features but cannot access system prompt management

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
- **Note:** All registered users are created as "student" type. Admin users are created automatically on server startup.

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

## System Prompt Management (Admin Only)

### Get System Prompt
- **GET** `/system-prompt`
- **Headers:** `Authorization: Bearer <admin_token>`
- **Response:**
```json
{
    "prompt": "string"
}
```

### Update System Prompt
- **PUT** `/system-prompt`
- **Headers:** `Authorization: Bearer <admin_token>`
- **Body:**
```json
{
    "prompt": "string"
}
```
- **Response:**
```json
{
    "prompt": "string"
}
```

**Note:** Only users with `user_type: "admin"` can access these endpoints. Students will receive a 403 Forbidden error.

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
- The current system prompt is automatically added as the first message
- The user's question becomes the chat title (truncated to 50 characters)

### Continuing Existing Chats
- When `chat_id` is provided, the system fetches the chat history
- All previous messages are included in the context sent to OpenAI
- The conversation maintains context across multiple exchanges

### Message History
- When `return_with_history=true`, all messages are returned sorted newest to oldest
- When `return_with_history=false`, only the AI response is returned
- Messages include role (user/assistant/system), content, and timestamp

### Dynamic System Prompt
- The system prompt is now managed dynamically through the API
- Only admins can view or update the system prompt
- Changes to the system prompt affect all new conversations immediately

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `first_name`: User's first name (optional)
- `last_name`: User's last name (optional)
- `user_type`: "admin" or "student"
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
- `403`: Forbidden (insufficient permissions - admin required)
- `404`: Not found (chat not found)
- `500`: Internal server error

## Security Features

1. **Password Hashing**: Uses bcrypt for secure password storage
2. **JWT Tokens**: Secure token-based authentication
3. **User Isolation**: Users can only access their own chats
4. **Role-Based Access**: Admin-only endpoints for system prompt management
5. **Input Validation**: All inputs are validated using Pydantic models

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
# Create .env file with admin credentials
python create_env.py

# Edit the .env file with your OpenAI API key
nano .env
```

3. Run the server:
```bash
python -m uvicorn chatbot.server:app --reload
```

4. Check the console output for admin creation messages:
```
✅ Admin user created successfully!
   Username: admin_user
   Email: admin@oui.edu.ng
   Name: Admin Officer
   Password: [generated-password]
   User Type: admin
```

5. Test the API:
```bash
python test_api.py
```

6. Test automatic admin creation:
```bash
python test_admin_creation.py
```

7. Run all tests:
```bash
# Option 1: Python test runner (with detailed output)
python run_all_tests.py

# Option 2: Bash script (simple)
chmod +x run_tests.sh
./run_tests.sh

# Option 3: Individual tests
python create_env.py
python reset_database.py
python test_api.py
python test_admin_creation.py
python test_curl_auto.py
```

**Note:** If you encounter database schema errors, you can reset the database:
```bash
python reset_database.py
```

## Example Usage

### Creating a User (Student)
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student",
    "email": "student@example.com",
    "first_name": "John",
    "last_name": "Student",
    "password": "securepassword"
  }'
```

**Note:** Admin users are created automatically on server startup using environment variables.

### Updating System Prompt (Admin Only)
```bash
curl -X PUT "http://localhost:8000/system-prompt" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "You are a helpful AI assistant specialized in helping students with their questions."
  }'
```

## Legacy Endpoints

The following endpoints are maintained for backward compatibility:
- `POST /` - FAQ query endpoint
- `POST /generate-response/` - Legacy AI response endpoint

## Environment Variables

The following environment variables can be configured in your `.env` file:

### Required
- `OPENAI_API_KEY`: Your OpenAI API key

### Optional
- `OPENAI_MODEL_NAME`: OpenAI model to use (default: gpt-3.5-turbo)
- `ADMIN_FIRST_NAME`: Admin first name (default: Admin)
- `ADMIN_LAST_NAME`: Admin last name (default: Officer)
- `ADMIN_USERNAME`: Admin username (default: admin_user)
- `ADMIN_EMAIL`: Admin email (default: admin@oui.edu.ng)
- `ADMIN_PASSWORD`: Admin password (auto-generated if not provided)
- `JWT_SECRET_KEY`: JWT secret key (default: development key)
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry time (default: 30)

## Notes

- The database file (`chatbot.db`) is created automatically on first run
- An admin account is automatically created on server startup if it doesn't exist
- If `ADMIN_PASSWORD` is not set, a secure random password is generated and displayed
- JWT tokens expire after 30 minutes (configurable)
- The system prompt is now managed dynamically through the API
- Only admins can modify the system prompt
- All timestamps are in UTC 
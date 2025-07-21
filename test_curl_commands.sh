#!/bin/bash

# Base URL
BASE_URL="http://0.0.0.0:8000"

echo "=== Testing Chatbot API with curl ==="

# 1. Register a new admin user
echo "1. Registering admin user..."
curl --location --request POST "$BASE_URL/register" \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "miraclem",
    "email": "blueprime91@gmail.com",
    "first_name": "Miracle",
    "last_name": "Adebunmi",
    "password": "Ojuade9me"
}'

echo -e "\n\n"

# 2. Login to get token
echo "2. Logging in to get token..."
TOKEN_RESPONSE=$(curl --location --request POST "$BASE_URL/login" \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "miraclem",
    "password": "Ojuade9me"
}')

echo "Token response: $TOKEN_RESPONSE"

# Extract token (you'll need to manually copy this)
echo "Please copy the access_token from the response above"

echo -e "\n\n"

# 3. Get system prompt (replace YOUR_TOKEN_HERE with actual token)
echo "3. Getting system prompt..."
curl --location --request GET "$BASE_URL/system-prompt" \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_TOKEN_HERE'

echo -e "\n\n"

# 4. Update system prompt (replace YOUR_TOKEN_HERE with actual token)
echo "4. Updating system prompt..."
curl --location --request PUT "$BASE_URL/system-prompt" \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_TOKEN_HERE' \
--data-raw '{
    "prompt": "You are a helpful AI assistant created by OUI. Be friendly and educational."
}'

echo -e "\n\n"

# 5. Test chat functionality (replace YOUR_TOKEN_HERE with actual token)
echo "5. Testing chat functionality..."
curl --location --request POST "$BASE_URL/get_ai_response" \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer YOUR_TOKEN_HERE' \
--data-raw '{
    "chat_id": null,
    "user_question": "Hello, how are you?",
    "return_with_history": true
}'

echo -e "\n\n=== Test completed ===" 
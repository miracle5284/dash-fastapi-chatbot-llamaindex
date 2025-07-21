#!/usr/bin/env python3
"""
Test script for the new chatbot API functionality
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_authentication():
    """Test user registration and login"""
    print("=== Testing Authentication ===")
    
    # Test user registration
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print(f"Register response: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"User created: {user_data['username']} - {user_data['first_name']} {user_data['last_name']}")
    
    # Test login
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Login response: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        print(f"Token received: {token_data['access_token'][:20]}...")
        return token_data['access_token']
    
    return None

def test_chat_functionality(token):
    """Test chat functionality"""
    print("\n=== Testing Chat Functionality ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test creating a new chat
    new_chat_data = {
        "chat_id": None,
        "user_question": "Hello, how are you?",
        "return_with_history": True
    }
    
    response = requests.post(f"{BASE_URL}/get_ai_response", json=new_chat_data, headers=headers)
    print(f"New chat response: {response.status_code}")
    if response.status_code == 200:
        chat_data = response.json()
        print(f"Chat ID: {chat_data['chat_id']}")
        print(f"AI Response: {chat_data['response'][:100]}...")
        print(f"Messages count: {len(chat_data['messages']) if chat_data['messages'] else 0}")
        
        # Test continuing the same chat
        continue_chat_data = {
            "chat_id": chat_data['chat_id'],
            "user_question": "What can you help me with?",
            "return_with_history": False
        }
        
        response = requests.post(f"{BASE_URL}/get_ai_response", json=continue_chat_data, headers=headers)
        print(f"Continue chat response: {response.status_code}")
        if response.status_code == 200:
            continue_data = response.json()
            print(f"AI Response: {continue_data['response'][:100]}...")
        
        return chat_data['chat_id']
    
    return None

def test_get_chats(token):
    """Test getting all chats"""
    print("\n=== Testing Get Chats ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/chats", headers=headers)
    print(f"Get chats response: {response.status_code}")
    if response.status_code == 200:
        chats_data = response.json()
        print(f"Found {len(chats_data['chats'])} chats")
        for chat in chats_data['chats']:
            print(f"Chat ID: {chat['id']}, Title: {chat['title']}, Messages: {len(chat['messages'])}")

def main():
    """Main test function"""
    print("Starting API tests...")
    
    # Test authentication
    token = test_authentication()
    if not token:
        print("Authentication failed!")
        return
    
    # Test chat functionality
    chat_id = test_chat_functionality(token)
    
    # Test getting all chats
    test_get_chats(token)
    
    print("\n=== Tests completed ===")

if __name__ == "__main__":
    main() 
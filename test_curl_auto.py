#!/usr/bin/env python3
"""
Automated curl-like testing script for the chatbot API
"""

import requests
import json

# Base URL
BASE_URL = "http://0.0.0.0:8000"

def test_api():
    """Test the API endpoints automatically"""
    
    print("=== Testing Chatbot API ===")
    
    # 1. Register admin user
    print("\n1. Registering admin user...")
    register_data = {
        "username": "miraclem",
        "email": "blueprime91@gmail.com",
        "first_name": "Miracle",
        "last_name": "Adebunmi",
        "password": "Ojuade9me"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print(f"Register response: {response.status_code}")
    if response.status_code == 200:
        print("✅ User registered successfully")
    elif response.status_code == 400:
        print("ℹ️  User already exists")
    else:
        print(f"❌ Registration failed: {response.text}")
    
    # 2. Login to get token
    print("\n2. Logging in...")
    login_data = {
        "username": "miraclem",
        "password": "Ojuade9me"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Login response: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data['access_token']
        print(f"✅ Login successful, token: {token[:20]}...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Get system prompt
        print("\n3. Getting system prompt...")
        response = requests.get(f"{BASE_URL}/system-prompt", headers=headers)
        print(f"Get prompt response: {response.status_code}")
        if response.status_code == 200:
            prompt_data = response.json()
            print(f"✅ Current prompt: {prompt_data['prompt'][:100]}...")
        else:
            print(f"❌ Failed to get prompt: {response.text}")
        
        # 4. Update system prompt
        print("\n4. Updating system prompt...")
        update_data = {
            "prompt": "You are a helpful AI assistant created by OUI. Be friendly and educational."
        }
        
        response = requests.put(f"{BASE_URL}/system-prompt", json=update_data, headers=headers)
        print(f"Update prompt response: {response.status_code}")
        if response.status_code == 200:
            print("✅ System prompt updated successfully!")
        else:
            print(f"❌ Failed to update prompt: {response.text}")
        
        # 5. Test chat functionality
        print("\n5. Testing chat functionality...")
        chat_data = {
            "chat_id": None,
            "user_question": "Hello, how are you?",
            "return_with_history": True
        }
        
        response = requests.post(f"{BASE_URL}/get_ai_response", json=chat_data, headers=headers)
        print(f"Chat response: {response.status_code}")
        if response.status_code == 200:
            chat_response = response.json()
            print(f"✅ Chat successful!")
            print(f"Chat ID: {chat_response['chat_id']}")
            print(f"AI Response: {chat_response['response'][:100]}...")
        else:
            print(f"❌ Chat failed: {response.text}")
        
        # 6. Get user info
        print("\n6. Getting user info...")
        response = requests.get(f"{BASE_URL}/me", headers=headers)
        print(f"User info response: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ User: {user_data['username']} ({user_data['user_type']})")
            print(f"Name: {user_data['first_name']} {user_data['last_name']}")
            print(f"Email: {user_data['email']}")
        else:
            print(f"❌ Failed to get user info: {response.text}")
        
    else:
        print(f"❌ Login failed: {response.text}")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    test_api() 
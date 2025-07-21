#!/usr/bin/env python3
"""
Test script for automatic admin creation functionality
"""

import requests
import json
import os

# API base URL
BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Test logging in with the automatically created admin account"""
    print("=== Testing Automatic Admin Login ===")
    
    # Get admin password from environment
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    admin_password = os.getenv("ADMIN_PASSWORD", "admin_user")
    
    # Try to login with the admin credentials from .env
    admin_login_data = {
        "username": "admin_user",
        "password": admin_password
    }
    
    response = requests.post(f"{BASE_URL}/login", json=admin_login_data)
    print(f"Admin login response: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"✅ Admin login successful!")
        print(f"Token received: {token_data['access_token'][:20]}...")
        return token_data['access_token']
    else:
        print(f"❌ Admin login failed: {response.text}")
        return None

def test_admin_access(token):
    """Test admin-specific functionality"""
    print("\n=== Testing Admin Access ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test getting current user info
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"Get user info response: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"User: {user_data['username']} ({user_data['user_type']})")
        print(f"Name: {user_data['first_name']} {user_data['last_name']}")
        print(f"Email: {user_data['email']}")
    
    # Test system prompt access (admin only)
    response = requests.get(f"{BASE_URL}/system-prompt", headers=headers)
    print(f"Get system prompt response: {response.status_code}")
    if response.status_code == 200:
        prompt_data = response.json()
        print(f"Current system prompt: {prompt_data['prompt'][:100]}...")
    
    # Test updating system prompt (admin only)
    new_prompt = "You are an AI assistant created by OUI. Be helpful and professional."
    update_data = {"prompt": new_prompt}
    
    response = requests.put(f"{BASE_URL}/system-prompt", json=update_data, headers=headers)
    print(f"Update system prompt response: {response.status_code}")
    if response.status_code == 200:
        print("✅ System prompt updated successfully!")

def test_chat_with_admin(token):
    """Test chat functionality with admin account"""
    print("\n=== Testing Chat with Admin ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test creating a new chat
    new_chat_data = {
        "chat_id": None,
        "user_question": "Hello, I'm the admin user. How are you?",
        "return_with_history": True
    }
    
    response = requests.post(f"{BASE_URL}/get_ai_response", json=new_chat_data, headers=headers)
    print(f"New chat response: {response.status_code}")
    if response.status_code == 200:
        chat_data = response.json()
        print(f"Chat ID: {chat_data['chat_id']}")
        print(f"AI Response: {chat_data['response'][:100]}...")
        print(f"Messages count: {len(chat_data['messages']) if chat_data['messages'] else 0}")

def main():
    """Main test function"""
    print("Testing Automatic Admin Creation...")
    print("Make sure the server is running and check the console for admin creation messages.")
    
    # Test admin login
    token = test_admin_login()
    if not token:
        print("\n❌ Admin login failed. Check if the server started properly and admin was created.")
        print("Look for admin creation messages in the server console.")
        return
    
    # Test admin access
    test_admin_access(token)
    
    # Test chat functionality
    test_chat_with_admin(token)
    
    print("\n=== Admin Creation Test Completed ===")

if __name__ == "__main__":
    main() 
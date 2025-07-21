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
    
    # Test admin user registration (will be created as student)
    admin_data = {
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "password": "adminpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=admin_data)
    print(f"Admin register response: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"Admin created: {user_data['username']} - {user_data['first_name']} {user_data['last_name']} ({user_data['user_type']})")
    
    # Test student user registration
    student_data = {
        "username": "student",
        "email": "student@example.com",
        "first_name": "John",
        "last_name": "Student",
        "password": "studentpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=student_data)
    print(f"Student register response: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"Student created: {user_data['username']} - {user_data['first_name']} {user_data['last_name']} ({user_data['user_type']})")
    
    # Test admin login
    admin_login_data = {
        "username": "admin",
        "password": "adminpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=admin_login_data)
    print(f"Admin login response: {response.status_code}")
    if response.status_code == 200:
        admin_token_data = response.json()
        print(f"Admin token received: {admin_token_data['access_token'][:20]}...")
        return admin_token_data['access_token'], "admin"
    
    return None, None

def test_system_prompt_management(admin_token):
    """Test system prompt management (admin only)"""
    print("\n=== Testing System Prompt Management ===")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test getting current system prompt
    response = requests.get(f"{BASE_URL}/system-prompt", headers=headers)
    print(f"Get system prompt response: {response.status_code}")
    if response.status_code == 200:
        prompt_data = response.json()
        print(f"Current system prompt: {prompt_data['prompt'][:100]}...")
    
    # Test updating system prompt
    new_prompt = "You are a helpful AI assistant specialized in helping students with their questions. Be friendly and educational."
    update_data = {"prompt": new_prompt}
    
    response = requests.put(f"{BASE_URL}/system-prompt", json=update_data, headers=headers)
    print(f"Update system prompt response: {response.status_code}")
    if response.status_code == 200:
        update_data = response.json()
        print(f"Updated system prompt: {update_data['prompt'][:100]}...")
    
    # Test getting updated prompt
    response = requests.get(f"{BASE_URL}/system-prompt", headers=headers)
    print(f"Get updated prompt response: {response.status_code}")
    if response.status_code == 200:
        prompt_data = response.json()
        print(f"Updated system prompt: {prompt_data['prompt'][:100]}...")

def test_student_access_restriction():
    """Test that students cannot access admin functions"""
    print("\n=== Testing Student Access Restrictions ===")
    
    # Register and login as student
    student_data = {
        "username": "teststudent",
        "email": "teststudent@example.com",
        "first_name": "Test",
        "last_name": "Student",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=student_data)
    if response.status_code == 200:
        print("Test student created")
    
    # Login as student
    login_data = {
        "username": "teststudent",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    if response.status_code == 200:
        student_token = response.json()['access_token']
        print("Test student logged in")
        
        # Try to access admin-only endpoints
        headers = {"Authorization": f"Bearer {student_token}"}
        
        # Test getting system prompt (should fail)
        response = requests.get(f"{BASE_URL}/system-prompt", headers=headers)
        print(f"Student trying to get system prompt: {response.status_code}")
        if response.status_code == 403:
            print("✓ Student correctly blocked from getting system prompt")
        
        # Test updating system prompt (should fail)
        update_data = {"prompt": "This should fail"}
        response = requests.put(f"{BASE_URL}/system-prompt", json=update_data, headers=headers)
        print(f"Student trying to update system prompt: {response.status_code}")
        if response.status_code == 403:
            print("✓ Student correctly blocked from updating system prompt")

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
    admin_token, user_type = test_authentication()
    if not admin_token:
        print("Authentication failed!")
        return
    
    # Test system prompt management (admin only)
    test_system_prompt_management(admin_token)
    
    # Test student access restrictions
    test_student_access_restriction()
    
    # Test chat functionality
    chat_id = test_chat_functionality(admin_token)
    
    # Test getting all chats
    test_get_chats(admin_token)
    
    print("\n=== Tests completed ===")

if __name__ == "__main__":
    main() 
#!/bin/bash

echo "🚀 Running all tests for Chatbot API..."
echo "=========================================="

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Run all tests
echo "1. Creating environment file..."
python create_env.py

echo "2. Resetting database..."
python reset_database.py

echo "3. Running main API tests..."
python test_api.py

echo "4. Testing admin creation..."
python test_admin_creation.py

echo "5. Testing curl-like API calls..."
python test_curl_auto.py

echo "✅ All tests completed!" 
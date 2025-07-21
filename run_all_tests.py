#!/usr/bin/env python3
"""
Comprehensive test runner for the chatbot API
"""

import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and display results"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Running: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("✅ Output:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  Errors/Warnings:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Test Suite")
    print("=" * 60)
    
    # List of tests to run
    tests = [
        {
            "command": "python create_env.py",
            "description": "Create Environment File"
        },
        {
            "command": "python reset_database.py",
            "description": "Reset Database and Create Admin"
        },
        {
            "command": "python test_api.py",
            "description": "Run Main API Tests"
        },
        {
            "command": "python test_admin_creation.py",
            "description": "Test Admin Creation"
        },
        {
            "command": "python test_curl_auto.py",
            "description": "Test Curl-like API Calls"
        }
    ]
    
    # Track results
    passed = 0
    failed = 0
    
    # Run each test
    for test in tests:
        success = run_command(test["command"], test["description"])
        if success:
            passed += 1
        else:
            failed += 1
        
        # Small delay between tests
        time.sleep(1)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    exit(main()) 
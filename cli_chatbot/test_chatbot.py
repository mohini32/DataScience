#!/usr/bin/env python3
"""
Simple tests for the CLI chatbot
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from providers.simple_provider import SimpleProvider
from providers.gemini_provider import GeminiProvider
from chatbot import ConversationManager


def test_simple_provider():
    """Test the simple rule-based provider"""
    print("🧪 Testing Simple Provider...")
    
    provider = SimpleProvider()
    conversation = ConversationManager()
    
    # Test basic functionality
    assert provider.is_available(), "Simple provider should always be available"
    
    # Test greeting
    response = provider.chat("hello", conversation.get_history())
    assert response, "Should get a response to greeting"
    print(f"✅ Greeting test: {response}")
    
    # Test programming question
    conversation.add_message("user", "hello")
    conversation.add_message("assistant", response)
    
    response = provider.chat("I'm working on Python code", conversation.get_history())
    assert "programming" in response.lower() or "code" in response.lower(), "Should recognize programming context"
    print(f"✅ Programming test: {response}")
    
    print("✅ Simple Provider tests passed!\n")


def test_conversation_manager():
    """Test conversation management"""
    print("🧪 Testing Conversation Manager...")
    
    manager = ConversationManager(max_history=3)
    
    # Test adding messages
    manager.add_message("user", "Hello")
    manager.add_message("assistant", "Hi there!")
    manager.add_message("user", "How are you?")
    
    history = manager.get_history()
    assert len(history) == 3, f"Expected 3 messages, got {len(history)}"
    
    # Test history limit
    manager.add_message("assistant", "I'm good!")
    manager.add_message("user", "That's great!")
    
    history = manager.get_history()
    assert len(history) == 3, f"History should be limited to 3, got {len(history)}"
    assert history[0]["content"] == "How are you?", "Oldest message should be removed"
    
    # Test clear
    manager.clear_history()
    assert len(manager.get_history()) == 0, "History should be empty after clear"
    
    print("✅ Conversation Manager tests passed!\n")


def test_gemini_provider():
    """Test Gemini provider availability"""
    print("🧪 Testing Gemini Provider...")
    
    try:
        provider = GeminiProvider()
        if provider.is_available():
            print("✅ Gemini provider is available and configured")
        else:
            print("⚠️  Gemini provider not available (API key not set)")
    except Exception as e:
        print(f"⚠️  Gemini provider error: {str(e)}")
    
    print()


def main():
    """Run all tests"""
    print("🚀 Running CLI Chatbot Tests\n")
    
    try:
        test_simple_provider()
        test_conversation_manager()
        test_gemini_provider()
        
        print("🎉 All tests completed successfully!")
        print("\n💡 To try the chatbot:")
        print("   python chatbot.py")
        print("\n💡 To use Google Gemini (if you have an API key):")
        print("   python chatbot.py --provider gemini")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

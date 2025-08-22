"""
Simple rule-based chatbot provider
Completely free and works without any external APIs or heavy libraries!
"""

import random
import re
from typing import List, Dict

from chatbot import AIProvider


class SimpleProvider(AIProvider):
    """Simple rule-based chatbot provider"""
    
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello! How can I help you today?",
                "Hi there! What would you like to talk about?",
                "Hey! I'm here to chat with you.",
                "Greetings! How are you doing?",
            ],
            'goodbye': [
                "Goodbye! It was nice chatting with you.",
                "See you later! Have a great day!",
                "Bye! Feel free to come back anytime.",
                "Take care! Until next time!",
            ],
            'how_are_you': [
                "I'm doing well, thank you for asking! How are you?",
                "I'm great! Thanks for checking in. How about you?",
                "I'm doing fine! What about yourself?",
                "All good here! How's your day going?",
            ],
            'name': [
                "I'm a simple AI chatbot! You can call me Bot.",
                "I'm your friendly AI assistant. What's your name?",
                "I'm a chatbot created to help and chat with you!",
                "I'm an AI assistant. Nice to meet you!",
            ],
            'help': [
                "I'm here to chat with you! Ask me anything - about programming, general questions, or just have a conversation.",
                "I can help with various topics like coding, writing, or just casual conversation. What interests you?",
                "Feel free to ask me questions about technology, programming, or anything else you'd like to discuss!",
                "I'm here to assist! Whether you need help with code, want to brainstorm ideas, or just chat, I'm ready.",
            ],
            'programming': [
                "Programming is fascinating! What language are you working with?",
                "I love talking about code! Are you working on any interesting projects?",
                "Programming can be challenging but rewarding. What are you trying to build?",
                "Code is like poetry - it should be elegant and functional. What's your favorite language?",
            ],
            'default': [
                "That's interesting! Tell me more about that.",
                "I see! What do you think about that?",
                "Hmm, that's a good point. Can you elaborate?",
                "That sounds intriguing! What's your take on it?",
                "I'd love to hear more about your thoughts on this.",
                "That's a fascinating topic! What got you interested in it?",
                "Interesting perspective! How did you come to that conclusion?",
            ]
        }
        
        self.patterns = {
            'greeting': r'\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b',
            'goodbye': r'\b(bye|goodbye|see you|farewell|take care|later)\b',
            'how_are_you': r'\b(how are you|how\'re you|how do you do|what\'s up|how\'s it going)\b',
            'name': r'\b(what\'s your name|who are you|what are you|your name)\b',
            'help': r'\b(help|assist|support|what can you do)\b',
            'programming': r'\b(code|coding|program|programming|python|javascript|java|c\+\+|html|css|sql|algorithm|function|variable|loop|debug)\b',
        }
    
    def _classify_message(self, message: str) -> str:
        """Classify the user's message to determine response type"""
        message_lower = message.lower()
        
        for category, pattern in self.patterns.items():
            if re.search(pattern, message_lower, re.IGNORECASE):
                return category
        
        return 'default'
    
    def _get_contextual_response(self, message: str, history: List[Dict[str, str]]) -> str:
        """Generate a contextual response based on conversation history"""
        # Check if user mentioned their name in recent history
        user_name = None
        for msg in reversed(history[-5:]):  # Check last 5 messages
            if msg["role"] == "user":
                name_match = re.search(r'\b(?:i\'m|i am|my name is|call me)\s+(\w+)', msg["content"], re.IGNORECASE)
                if name_match:
                    user_name = name_match.group(1)
                    break
        
        category = self._classify_message(message)
        response = random.choice(self.responses[category])
        
        # Personalize response if we know the user's name
        if user_name and category in ['greeting', 'how_are_you']:
            response = response.replace("How are you?", f"How are you, {user_name}?")
            response = response.replace("How about you?", f"How about you, {user_name}?")
        
        return response
    
    def chat(self, message: str, history: List[Dict[str, str]]) -> str:
        """Generate a response using simple rules and patterns"""
        try:
            # Handle empty or very short messages
            if not message.strip() or len(message.strip()) < 2:
                return "I didn't quite catch that. Could you say that again?"
            
            # Generate contextual response
            response = self._get_contextual_response(message, history)
            
            # Add some variety based on conversation length
            if len(history) > 10:
                variety_responses = [
                    "We've been chatting for a while! ",
                    "I'm enjoying our conversation! ",
                    "This has been a great chat! ",
                ]
                if random.random() < 0.3:  # 30% chance
                    response = random.choice(variety_responses) + response
            
            return response
            
        except Exception as e:
            return f"I encountered an error: {str(e)}. Let's try again!"
    
    def is_available(self) -> bool:
        """Simple provider is always available"""
        return True

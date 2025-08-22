"""
Google Gemini API provider
Free tier available with generous quotas!
"""

import os
import time
from typing import List, Dict

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from chatbot import AIProvider


class GeminiProvider(AIProvider):
    """Google Gemini API provider"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.model = None
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Rate limiting: 1 second between requests
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Gemini client"""
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Generative AI not available. Install with: pip install google-generativeai")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        try:
            # Configure the API
            genai.configure(api_key=self.api_key)
            
            # Initialize the model
            self.model = genai.GenerativeModel('gemini-pro')
            
            print("✅ Google Gemini API initialized successfully!")
            
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini API: {str(e)}")
    
    def _rate_limit(self):
        """Simple rate limiting to avoid hitting API limits"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _format_conversation(self, message: str, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Format conversation history for Gemini API"""
        # Gemini expects alternating user/model messages
        formatted_history = []
        
        # Add conversation history
        for msg in history[:-1]:  # Exclude the current message as it's added separately
            if msg["role"] == "user":
                formatted_history.append({
                    "role": "user",
                    "parts": [msg["content"]]
                })
            elif msg["role"] == "assistant":
                formatted_history.append({
                    "role": "model",
                    "parts": [msg["content"]]
                })
        
        return formatted_history
    
    def chat(self, message: str, history: List[Dict[str, str]]) -> str:
        """Generate a response using Gemini API"""
        if not self.model:
            raise Exception("Gemini model not initialized")
        
        try:
            # Apply rate limiting
            self._rate_limit()
            
            # Format conversation history
            formatted_history = self._format_conversation(message, history)
            
            # Start a chat session with history
            chat = self.model.start_chat(history=formatted_history)
            
            # Generate response
            response = chat.send_message(
                message,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=1000,
                )
            )
            
            return response.text
        
        except Exception as e:
            # Handle common API errors gracefully
            error_msg = str(e).lower()
            
            if "quota" in error_msg or "limit" in error_msg:
                return "⚠️ API quota exceeded. Please try again later or switch to the local Hugging Face provider."
            elif "api_key" in error_msg or "authentication" in error_msg:
                return "⚠️ API authentication failed. Please check your GOOGLE_API_KEY in the .env file."
            elif "safety" in error_msg:
                return "⚠️ Response was blocked due to safety filters. Please try rephrasing your question."
            else:
                return f"⚠️ API error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if the provider is available"""
        return GEMINI_AVAILABLE and self.model is not None and self.api_key is not None

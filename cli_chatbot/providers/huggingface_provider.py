"""
Hugging Face Transformers provider for local AI models
Completely free and works offline!
"""

import os
import warnings
from typing import List, Dict

# Suppress some warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning)

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

from chatbot import AIProvider


class HuggingFaceProvider(AIProvider):
    """Hugging Face Transformers provider for local models"""
    
    def __init__(self):
        self.model_name = os.getenv("HF_MODEL", "microsoft/DialoGPT-medium")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.model = None
        self.tokenizer = None
        self.generator = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Hugging Face model"""
        if not HF_AVAILABLE:
            raise ImportError("Hugging Face transformers not available. Install with: pip install transformers torch")
        
        try:
            print(f"🔄 Loading model: {self.model_name} (this may take a moment on first run)...")
            
            # Use a text generation pipeline for simplicity
            self.generator = pipeline(
                "text-generation",
                model=self.model_name,
                tokenizer=self.model_name,
                device=0 if torch.cuda.is_available() else -1,  # Use GPU if available
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                trust_remote_code=True
            )
            
            print("✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            print("💡 Trying with a smaller, more reliable model...")
            
            # Fallback to a smaller, more reliable model
            try:
                self.model_name = "gpt2"
                self.generator = pipeline(
                    "text-generation",
                    model=self.model_name,
                    device=0 if torch.cuda.is_available() else -1,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                print("✅ Fallback model (GPT-2) loaded successfully!")
            except Exception as fallback_error:
                raise Exception(f"Failed to load any model: {str(fallback_error)}")
    
    def _format_conversation(self, message: str, history: List[Dict[str, str]]) -> str:
        """Format the conversation for the model"""
        # Create a conversation context
        conversation = ""
        
        # Add recent history (last few exchanges)
        recent_history = history[-6:] if len(history) > 6 else history
        
        for msg in recent_history:
            if msg["role"] == "user":
                conversation += f"Human: {msg['content']}\n"
            elif msg["role"] == "assistant":
                conversation += f"Assistant: {msg['content']}\n"
        
        # Add current message
        conversation += f"Human: {message}\nAssistant:"
        
        return conversation
    
    def chat(self, message: str, history: List[Dict[str, str]]) -> str:
        """Generate a response using the local model"""
        if not self.generator:
            raise Exception("Model not initialized")
        
        try:
            # Format the input
            prompt = self._format_conversation(message, history)
            
            # Generate response
            outputs = self.generator(
                prompt,
                max_new_tokens=150,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self.generator.tokenizer.eos_token_id,
                num_return_sequences=1,
                truncation=True
            )
            
            # Extract the response
            generated_text = outputs[0]["generated_text"]
            
            # Extract only the new part (after "Assistant:")
            if "Assistant:" in generated_text:
                response = generated_text.split("Assistant:")[-1].strip()
                
                # Clean up the response
                response = response.split("Human:")[0].strip()  # Remove any follow-up human text
                response = response.split("\n")[0].strip()      # Take first line for cleaner responses
                
                if not response:
                    response = "I'm not sure how to respond to that. Could you try rephrasing your question?"
                
                return response
            else:
                return "I'm having trouble generating a response. Please try again."
        
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if the provider is available"""
        return HF_AVAILABLE and self.generator is not None

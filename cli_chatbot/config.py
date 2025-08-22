"""
Configuration management for the CLI chatbot
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the chatbot"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """Load configuration from environment variables"""
        # API Keys
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        
        # Provider settings
        self.ai_provider = os.getenv("AI_PROVIDER", "huggingface")
        self.hf_model = os.getenv("HF_MODEL", "microsoft/DialoGPT-medium")
        
        # Chat settings
        self.max_history = int(os.getenv("MAX_HISTORY", "10"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        
        # Validate configuration
        self.validate_config()
    
    def validate_config(self):
        """Validate the configuration"""
        # Validate provider
        valid_providers = ["simple", "gemini", "huggingface"]
        if self.ai_provider not in valid_providers:
            raise ValueError(f"Invalid AI_PROVIDER: {self.ai_provider}. Must be one of: {valid_providers}")
        
        # Validate numeric values
        if self.max_history < 1:
            raise ValueError("MAX_HISTORY must be at least 1")
        
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("TEMPERATURE must be between 0.0 and 2.0")
        
        # Provider-specific validation
        if self.ai_provider == "gemini" and not self.google_api_key:
            print("⚠️  Warning: GOOGLE_API_KEY not set. Gemini provider will not work.")
    
    def get_provider_config(self) -> Dict[str, Any]:
        """Get configuration for the current provider"""
        if self.ai_provider == "simple":
            return {
                "temperature": self.temperature
            }
        elif self.ai_provider == "gemini":
            return {
                "api_key": self.google_api_key,
                "temperature": self.temperature
            }
        elif self.ai_provider == "huggingface":
            return {
                "model_name": self.hf_model,
                "temperature": self.temperature
            }
        else:
            raise ValueError(f"Unknown provider: {self.ai_provider}")
    
    def display_config(self):
        """Display current configuration"""
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        
        table = Table(title="Current Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("AI Provider", self.ai_provider)
        table.add_row("Max History", str(self.max_history))
        table.add_row("Temperature", str(self.temperature))

        if self.ai_provider == "simple":
            table.add_row("Mode", "Rule-based (No API required)")
        elif self.ai_provider == "gemini":
            api_key_display = "✅ Set" if self.google_api_key else "❌ Not set"
            table.add_row("Google API Key", api_key_display)
        elif self.ai_provider == "huggingface":
            table.add_row("HF Model", self.hf_model)
        
        console.print(table)


# Global config instance
config = Config()

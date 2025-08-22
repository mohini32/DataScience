#!/usr/bin/env python3
"""
CLI Chatbot with multiple AI provider support
"""

import os
import sys
from typing import List, Dict, Optional
from abc import ABC, abstractmethod

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config import config

console = Console()


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def chat(self, message: str, history: List[Dict[str, str]]) -> str:
        """Send a message and get a response"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is properly configured and available"""
        pass


class ConversationManager:
    """Manages conversation history and context"""
    
    def __init__(self, max_history: int = 10):
        self.history: List[Dict[str, str]] = []
        self.max_history = max_history
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.history.append({"role": role, "content": content})
        
        # Keep only the last max_history messages
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def clear_history(self):
        """Clear the conversation history"""
        self.history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history"""
        return self.history.copy()


class ChatBot:
    """Main chatbot class"""
    
    def __init__(self, provider: AIProvider):
        self.provider = provider
        self.conversation = ConversationManager(
            max_history=int(os.getenv("MAX_HISTORY", "10"))
        )
        self.running = True
    
    def display_welcome(self):
        """Display welcome message"""
        provider_name = type(self.provider).__name__.replace("Provider", "")
        welcome_text = f"""
# 🤖 CLI Chatbot

Welcome! I'm your AI assistant powered by **{provider_name}**.

## Available Commands:
- **exit** or **quit**: Exit the chatbot
- **clear**: Clear conversation history
- **history**: Show conversation history
- **save**: Save conversation to file
- **help**: Show this help message

## Tips:
- Ask me anything! I can help with coding, writing, analysis, and more
- Use **clear** to start fresh if the conversation gets too long
- Type **history** to see our conversation so far

Just type your message and press Enter to start chatting!
        """
        console.print(Panel(Markdown(welcome_text), title="Welcome", border_style="blue"))
    
    def display_help(self):
        """Display help information"""
        help_text = """
# Available Commands

- **exit** or **quit**: Exit the chatbot
- **clear**: Clear conversation history
- **history**: Show conversation history
- **save**: Save conversation to file
- **help**: Show this help message

## Usage Tips:
- Ask questions naturally - I understand context from our conversation
- Use **clear** if you want to start a new topic
- Save interesting conversations with **save**

Just type your message to chat with the AI!
        """
        console.print(Panel(Markdown(help_text), title="Help", border_style="green"))

    def display_history(self):
        """Display conversation history"""
        if not self.conversation.history:
            console.print("📝 No conversation history yet.", style="yellow")
            return

        console.print(f"\n📚 Conversation History ({len(self.conversation.history)} messages):", style="bold blue")

        for i, msg in enumerate(self.conversation.history, 1):
            role = "You" if msg["role"] == "user" else "AI"
            style = "blue" if msg["role"] == "user" else "green"

            # Truncate long messages for display
            content = msg["content"]
            if len(content) > 100:
                content = content[:97] + "..."

            console.print(f"{i:2d}. [{style}]{role}:[/{style}] {content}")

    def save_conversation(self):
        """Save conversation to a file"""
        if not self.conversation.history:
            console.print("📝 No conversation to save.", style="yellow")
            return

        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Chatbot Conversation - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")

                for msg in self.conversation.history:
                    role = "You" if msg["role"] == "user" else "AI"
                    f.write(f"{role}: {msg['content']}\n\n")

            console.print(f"💾 Conversation saved to: {filename}", style="bold green")

        except Exception as e:
            console.print(f"❌ Error saving conversation: {str(e)}", style="bold red")
    
    def handle_command(self, user_input: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        command = user_input.lower().strip()

        if command in ['exit', 'quit']:
            console.print("👋 Goodbye!", style="bold blue")
            self.running = False
            return True

        elif command == 'clear':
            self.conversation.clear_history()
            console.print("🧹 Conversation history cleared!", style="bold green")
            return True

        elif command == 'history':
            self.display_history()
            return True

        elif command == 'save':
            self.save_conversation()
            return True

        elif command == 'help':
            self.display_help()
            return True

        elif command == 'config':
            config.display_config()
            return True

        return False
    
    def chat_loop(self):
        """Main chat loop"""
        self.display_welcome()
        
        if not self.provider.is_available():
            console.print("❌ AI provider is not available. Please check your configuration.", style="bold red")
            return
        
        while self.running:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
                
                if not user_input.strip():
                    continue
                
                # Handle commands
                if self.handle_command(user_input):
                    continue
                
                # Add user message to history
                self.conversation.add_message("user", user_input)
                
                # Show thinking indicator
                with console.status("[bold green]AI is thinking...", spinner="dots"):
                    try:
                        # Get AI response
                        response = self.provider.chat(user_input, self.conversation.get_history())
                        
                        # Add AI response to history
                        self.conversation.add_message("assistant", response)
                        
                        # Display AI response
                        console.print(f"\n[bold green]AI:[/bold green]")
                        console.print(Panel(Markdown(response), border_style="green"))
                        
                    except Exception as e:
                        console.print(f"❌ Error getting AI response: {str(e)}", style="bold red")
            
            except KeyboardInterrupt:
                console.print("\n👋 Goodbye!", style="bold blue")
                break
            except EOFError:
                console.print("\n👋 Goodbye!", style="bold blue")
                break


@click.command()
@click.option('--provider', default=None, help='AI provider to use (gemini, huggingface)')
def main(provider):
    """CLI Chatbot with multiple AI provider support"""
    
    # Determine which provider to use
    if not provider:
        provider = os.getenv("AI_PROVIDER", "simple")

    console.print(f"🚀 Starting chatbot with provider: {provider}", style="bold blue")

    # Import and initialize the appropriate provider
    try:
        if provider == "simple":
            from providers.simple_provider import SimpleProvider
            ai_provider = SimpleProvider()
        elif provider == "gemini":
            from providers.gemini_provider import GeminiProvider
            ai_provider = GeminiProvider()
        elif provider == "huggingface":
            from providers.huggingface_provider import HuggingFaceProvider
            ai_provider = HuggingFaceProvider()
        else:
            console.print(f"❌ Unknown provider: {provider}", style="bold red")
            console.print("Available providers: simple, gemini, huggingface", style="yellow")
            sys.exit(1)
        
        # Start the chatbot
        chatbot = ChatBot(ai_provider)
        chatbot.chat_loop()
        
    except ImportError as e:
        console.print(f"❌ Failed to import provider: {str(e)}", style="bold red")
        console.print("Make sure all dependencies are installed: pip install -r requirements.txt", style="yellow")
        sys.exit(1)
    except Exception as e:
        console.print(f"❌ Error starting chatbot: {str(e)}", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main()

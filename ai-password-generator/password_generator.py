#!/usr/bin/env python3
"""
AI Password Generator MVP
Simple, quick, and functional password generator with AI-like intelligence
"""

import random
import string
import secrets
import argparse
from typing import List, Dict


class PasswordGenerator:
    """Smart password generator with AI-like patterns"""
    
    def __init__(self):
        self.patterns = {
            'secure': {
                'length': 16,
                'use_uppercase': True,
                'use_lowercase': True,
                'use_numbers': True,
                'use_symbols': True,
                'avoid_ambiguous': True
            },
            'memorable': {
                'length': 12,
                'use_uppercase': True,
                'use_lowercase': True,
                'use_numbers': True,
                'use_symbols': False,
                'avoid_ambiguous': True
            },
            'simple': {
                'length': 8,
                'use_uppercase': True,
                'use_lowercase': True,
                'use_numbers': True,
                'use_symbols': False,
                'avoid_ambiguous': True
            },
            'complex': {
                'length': 20,
                'use_uppercase': True,
                'use_lowercase': True,
                'use_numbers': True,
                'use_symbols': True,
                'avoid_ambiguous': False
            }
        }
        
        # Common words for memorable passwords
        self.words = [
            'Apple', 'Beach', 'Cloud', 'Dream', 'Eagle', 'Fire', 'Green', 'Happy',
            'Island', 'Jump', 'King', 'Light', 'Moon', 'Night', 'Ocean', 'Peace',
            'Quick', 'River', 'Star', 'Tree', 'Unity', 'Voice', 'Water', 'Xray',
            'Yellow', 'Zebra', 'Magic', 'Power', 'Swift', 'Brave'
        ]
    
    def get_character_sets(self, config: Dict) -> str:
        """Get character sets based on configuration"""
        chars = ""
        
        if config['use_lowercase']:
            chars += string.ascii_lowercase
        
        if config['use_uppercase']:
            chars += string.ascii_uppercase
        
        if config['use_numbers']:
            chars += string.digits
        
        if config['use_symbols']:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if config['avoid_ambiguous']:
            # Remove ambiguous characters
            ambiguous = "0O1lI"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        return chars
    
    def generate_random_password(self, config: Dict) -> str:
        """Generate a random password based on configuration"""
        chars = self.get_character_sets(config)
        
        if not chars:
            raise ValueError("No character sets selected")
        
        # Use secrets for cryptographically secure random generation
        password = ''.join(secrets.choice(chars) for _ in range(config['length']))
        
        return password
    
    def generate_memorable_password(self, config: Dict) -> str:
        """Generate a memorable password using words and numbers"""
        # Pick 2-3 random words
        num_words = min(3, max(2, config['length'] // 4))
        selected_words = random.sample(self.words, num_words)
        
        # Add numbers
        if config['use_numbers']:
            number = random.randint(10, 999)
            selected_words.append(str(number))
        
        # Join with separator
        separators = ['', '-', '_'] if not config['use_symbols'] else ['', '-', '_', '!', '@']
        separator = random.choice(separators)
        
        password = separator.join(selected_words)
        
        # Adjust case
        if config['use_uppercase'] and config['use_lowercase']:
            # Mix case randomly
            password = ''.join(c.upper() if random.random() > 0.5 else c.lower() 
                             for c in password if c.isalpha()) + \
                      ''.join(c for c in password if not c.isalpha())
        elif config['use_uppercase']:
            password = password.upper()
        elif config['use_lowercase']:
            password = password.lower()
        
        return password
    
    def generate_pattern_password(self, pattern_name: str) -> str:
        """Generate password using predefined patterns"""
        if pattern_name not in self.patterns:
            raise ValueError(f"Unknown pattern: {pattern_name}")
        
        config = self.patterns[pattern_name]
        
        if pattern_name == 'memorable':
            return self.generate_memorable_password(config)
        else:
            return self.generate_random_password(config)
    
    def generate_custom_password(self, length: int = 12, uppercase: bool = True, 
                                lowercase: bool = True, numbers: bool = True, 
                                symbols: bool = False, avoid_ambiguous: bool = True) -> str:
        """Generate custom password with specific requirements"""
        config = {
            'length': length,
            'use_uppercase': uppercase,
            'use_lowercase': lowercase,
            'use_numbers': numbers,
            'use_symbols': symbols,
            'avoid_ambiguous': avoid_ambiguous
        }
        
        return self.generate_random_password(config)
    
    def analyze_password_strength(self, password: str) -> Dict:
        """Analyze password strength"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
        # Character variety
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 2
        else:
            feedback.append("Add special characters for better security")
        
        # Determine strength
        if score >= 6:
            strength = "Strong"
        elif score >= 4:
            strength = "Medium"
        else:
            strength = "Weak"
        
        return {
            'strength': strength,
            'score': score,
            'max_score': 7,
            'feedback': feedback
        }


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="AI Password Generator MVP")
    parser.add_argument('--pattern', choices=['secure', 'memorable', 'simple', 'complex'], 
                       default='secure', help='Password pattern to use')
    parser.add_argument('--length', type=int, default=12, help='Password length')
    parser.add_argument('--count', type=int, default=1, help='Number of passwords to generate')
    parser.add_argument('--no-symbols', action='store_true', help='Exclude symbols')
    parser.add_argument('--analyze', type=str, help='Analyze strength of given password')
    
    args = parser.parse_args()
    
    generator = PasswordGenerator()
    
    # Analyze password if requested
    if args.analyze:
        analysis = generator.analyze_password_strength(args.analyze)
        print(f"\n🔍 Password Analysis for: {args.analyze}")
        print(f"Strength: {analysis['strength']} ({analysis['score']}/{analysis['max_score']})")
        if analysis['feedback']:
            print("Suggestions:")
            for suggestion in analysis['feedback']:
                print(f"  • {suggestion}")
        return
    
    # Generate passwords
    print(f"\n🔐 AI Password Generator - {args.pattern.title()} Pattern")
    print("=" * 50)
    
    for i in range(args.count):
        if args.pattern in generator.patterns:
            password = generator.generate_pattern_password(args.pattern)
        else:
            password = generator.generate_custom_password(
                length=args.length,
                symbols=not args.no_symbols
            )
        
        # Analyze generated password
        analysis = generator.analyze_password_strength(password)
        
        print(f"\nPassword {i+1}: {password}")
        print(f"Strength: {analysis['strength']} ({analysis['score']}/{analysis['max_score']})")
    
    print(f"\n💡 Tips:")
    print("  • Use different passwords for different accounts")
    print("  • Store passwords in a password manager")
    print("  • Enable 2FA when possible")


if __name__ == "__main__":
    main()

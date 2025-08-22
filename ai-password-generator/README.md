# AI Password Generator MVP

A simple, intelligent password generator that creates secure passwords using AI-like patterns and analysis.

## Features

- **Multiple Patterns**: Secure, memorable, simple, and complex password patterns
- **Smart Analysis**: Real-time password strength analysis with feedback
- **Customizable**: Adjust length, character sets, and complexity
- **Secure**: Uses cryptographically secure random generation
- **No Dependencies**: Pure Python - no external libraries needed

## Quick Start

### Command Line Interface
```bash
# Generate a secure password (default)
python password_generator.py

# Generate memorable passwords
python password_generator.py --pattern memorable

# Generate multiple passwords
python password_generator.py --count 5

# Custom length
python password_generator.py --length 16

# Analyze existing password
python password_generator.py --analyze "mypassword123"
```

### Web Interface
```bash
# Start the web server
python web_app.py

# Open browser to http://localhost:8000
```
The web interface provides an easy-to-use GUI for generating and analyzing passwords.

## Password Patterns

- **secure** (default): 16 chars, all character types, avoids ambiguous chars
- **memorable**: 12 chars, uses words + numbers, easier to remember
- **simple**: 8 chars, basic alphanumeric, good for simple accounts
- **complex**: 20 chars, maximum security with all symbols

## Examples

```bash
# Secure password
python password_generator.py --pattern secure

# Memorable password
python password_generator.py --pattern memorable

# Simple password without symbols
python password_generator.py --pattern simple --no-symbols

# Generate 3 complex passwords
python password_generator.py --pattern complex --count 3
```

## Password Strength Analysis

The tool analyzes passwords based on:
- Length (8+ characters recommended)
- Character variety (uppercase, lowercase, numbers, symbols)
- Overall security score

## Security Features

- Uses `secrets` module for cryptographically secure randomness
- Avoids ambiguous characters (0, O, 1, l, I) by default
- Provides strength analysis and improvement suggestions
- Generates truly random passwords, not predictable patterns

## Tips

- Use different passwords for different accounts
- Store passwords in a password manager
- Enable 2FA when possible
- Regularly update important passwords

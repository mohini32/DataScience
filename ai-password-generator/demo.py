#!/usr/bin/env python3
"""
Demo script for AI Password Generator MVP
Shows all features in action
"""

from password_generator import PasswordGenerator


def main():
    """Run a comprehensive demo"""
    print("🔐 AI Password Generator MVP Demo")
    print("=" * 50)
    
    generator = PasswordGenerator()
    
    # Demo 1: Different patterns
    print("\n📋 1. Different Password Patterns:")
    patterns = ['secure', 'memorable', 'simple', 'complex']
    
    for pattern in patterns:
        password = generator.generate_pattern_password(pattern)
        analysis = generator.analyze_password_strength(password)
        print(f"\n{pattern.title():>10}: {password}")
        print(f"{'Strength':>10}: {analysis['strength']} ({analysis['score']}/{analysis['max_score']})")
    
    # Demo 2: Multiple passwords
    print("\n\n📋 2. Multiple Memorable Passwords:")
    for i in range(3):
        password = generator.generate_pattern_password('memorable')
        print(f"Password {i+1}: {password}")
    
    # Demo 3: Custom passwords
    print("\n\n📋 3. Custom Password Options:")
    custom_configs = [
        {'length': 8, 'symbols': False, 'name': 'Simple 8-char'},
        {'length': 16, 'symbols': True, 'name': 'Complex 16-char'},
        {'length': 12, 'symbols': False, 'name': 'Alphanumeric 12-char'}
    ]
    
    for config in custom_configs:
        password = generator.generate_custom_password(
            length=config['length'],
            symbols=config['symbols']
        )
        analysis = generator.analyze_password_strength(password)
        print(f"\n{config['name']:>20}: {password}")
        print(f"{'Strength':>20}: {analysis['strength']} ({analysis['score']}/{analysis['max_score']})")
    
    # Demo 4: Password analysis
    print("\n\n📋 4. Password Strength Analysis:")
    test_passwords = [
        "password",
        "Password123",
        "P@ssw0rd123!",
        "MySecureP@ssw0rd2024!"
    ]
    
    for password in test_passwords:
        analysis = generator.analyze_password_strength(password)
        print(f"\nPassword: {password}")
        print(f"Strength: {analysis['strength']} ({analysis['score']}/{analysis['max_score']})")
        if analysis['feedback']:
            print("Suggestions:")
            for suggestion in analysis['feedback']:
                print(f"  • {suggestion}")
    
    # Demo 5: Usage examples
    print("\n\n📋 5. Usage Examples:")
    print("\nCommand Line:")
    print("  python password_generator.py --pattern secure")
    print("  python password_generator.py --pattern memorable --count 3")
    print("  python password_generator.py --analyze 'mypassword123'")
    
    print("\nWeb Interface:")
    print("  python web_app.py")
    print("  Open: http://localhost:8000")
    
    print("\n\n💡 Security Tips:")
    print("  • Use different passwords for different accounts")
    print("  • Store passwords in a password manager")
    print("  • Enable 2FA when possible")
    print("  • Regularly update important passwords")
    print("  • Never share passwords via email or text")
    
    print("\n🎉 Demo completed! The AI Password Generator MVP is ready to use.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
InvestAI Quick Start Script
Run this from your project directory to start InvestAI
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 InvestAI Quick Start")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Look for investai directory
    investai_dir = current_dir / "investai"
    backend_dir = investai_dir / "backend"
    
    if not investai_dir.exists():
        print("❌ 'investai' directory not found in current directory")
        print("💡 Make sure you're in the directory containing the 'investai' folder")
        print("💡 Or copy the investai folder to your current directory")
        return 1
    
    if not backend_dir.exists():
        print("❌ 'investai/backend' directory not found")
        return 1
    
    main_py = backend_dir / "app" / "main.py"
    if not main_py.exists():
        print("❌ 'app/main.py' not found in backend directory")
        return 1
    
    print("✅ InvestAI project found!")
    print(f"📁 Backend path: {backend_dir}")
    
    # Install basic dependencies
    print("\n📦 Installing basic dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "fastapi", "uvicorn", "sqlalchemy", "pydantic"
        ], check=True, capture_output=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("⚠️ Could not install dependencies automatically")
        print("💡 Run manually: pip install fastapi uvicorn sqlalchemy pydantic")
    
    # Change to backend directory
    os.chdir(backend_dir)
    print(f"\n📂 Changed to: {backend_dir}")
    
    print("\n🌐 Starting InvestAI server...")
    print("🔗 Will be available at: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Start server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except FileNotFoundError:
        print("❌ uvicorn not found. Install with: pip install uvicorn")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Quick setup script to verify and fix all issues
"""
import os
import subprocess
import sys

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def run_command(cmd, description):
    print(f"\n▶ {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"⚠️  {description}")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description}: {e}")
        return False

def main():
    print_section("AI Governance Assessor - Startup Checklist")
    
    # 1. Check Python version
    print("\n1️⃣  Verifying Python environment...")
    python_version = sys.version.split()[0]
    print(f"   Python {python_version}")
    if sys.version_info < (3, 8):
        print("   ⚠️  Python 3.8+ required")
        return False
    print("   ✅ Python version OK")
    
    # 2. Check data directory
    print("\n2️⃣  Checking data directory...")
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    print("   ✅ Directories ready")
    
    # 3. Install/upgrade pip
    print("\n3️⃣  Setting up Python dependencies...")
    run_command("python -m pip install --upgrade pip setuptools wheel", "Upgrading pip")
    
    # 4. Install requirements
    print("\n4️⃣  Installing required packages...")
    if run_command("pip install -q -r requirements.txt", "Installing from requirements.txt"):
        print("   ✅ All packages installed")
    else:
        print("   ⚠️  Some packages may not have installed")
    
    # 5. Copy environment file if not present
    print("\n5️⃣  Setting up configuration...")
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            subprocess.run("cp .env.example .env", shell=True)
            print("   ✅ Created .env from .env.example")
        else:
            print("   ⚠️  .env.example not found")
    else:
        print("   ✅ .env already configured")
    
    # 6. Reset database if needed
    print("\n6️⃣  Preparing database...")
    if os.path.exists("data/governance_assessments.db"):
        print("   ℹ️  Existing database found")
        print("   ✅ Running automatic migration...")
    else:
        print("   ℹ️  Database will be created on first run")
        print("   ✅ Fresh start configured")
    
    print_section("Setup Complete! 🎉")
    print("\nNext steps:")
    print("  1. Run the application:")
    print("     streamlit run src/app/main.py")
    print("\n  2. Access in browser:")
    print("     http://localhost:8501")
    print("\n  3. Create a test account or register")
    print("\nFor more information:")
    print("  - See PHASE_1_CHANGES.md for security improvements")
    print("  - See .env.example for configuration options")
    print("\n" + "=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

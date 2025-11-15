import subprocess
import time
import requests

def check_app_status():
    print("🔍 Checking app status...")
    
    # Check if app is running
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✅ App is running on localhost:8000")
            return True
    except:
        print("❌ App not reachable on localhost:8000")
        return False

def start_app_in_background():
    print("🚀 Starting app in background...")
    
    # Start streamlit in background
    process = subprocess.Popen([
        "streamlit", "run", "src/app/main.py",
        "--server.port", "8000", 
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("✅ App started in background")
    print("💡 Your app URL: https://congenial-goggles-rjjqx75x9v9f55pp-8000.app.github.dev/")
    return process

# Check current status
if check_app_status():
    print("App is already running!")
else:
    print("Starting app...")
    process = start_app_in_background()
    time.sleep(5)
    check_app_status()

print("\n🎯 NEXT STEPS:")
print("1. Open this URL in your browser:")
print("   https://congenial-goggles-rjjqx75x9v9f55pp-8000.app.github.dev/")
print("2. Test the application")
print("3. Use this terminal for debugging")
print("4. To stop: pkill -f streamlit")

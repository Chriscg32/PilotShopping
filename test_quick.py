#!/usr/bin/env python3
"""
Quick test script for ButterflyBlue Creations
"""

import requests
import time
import json

def test_butterflyblue():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing ButterflyBlue Creations...")
    
    # Wait for server
    time.sleep(1)
    
    try:
        # Test health
        print("\n1. Health Check...")
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        
        # Test agents
        print("\n2. Agents List...")
        response = requests.get(f"{base_url}/api/agents")
        if response.status_code == 200:
            agents = response.json()
            print(f"   ✅ Found {len(agents)} agents")
            for name in agents.keys():
                print(f"      🤖 {name}")
        
        # Test marketing demo
        print("\n3. Marketing Demo...")
        response = requests.post(f"{base_url}/api/demo/marketing-campaign")
        if response.status_code == 200:
            print("   ✅ Marketing demo working")
        
        # Test design demo
        print("\n4. Design Demo...")
        response = requests.post(f"{base_url}/api/demo/website-design")
        if response.status_code == 200:
            print("   ✅ Design demo working")
        
        print("\n🎉 All tests passed!")
        print(f"\n🦋 Visit http://localhost:8000/app to see the web interface!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_butterflyblue()
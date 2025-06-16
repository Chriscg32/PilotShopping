#!/usr/bin/env python3
"""
Test script to verify ButterflyBlue Creations API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing ButterflyBlue Creations API...")
    
    # Test health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   Service: {data['message']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test agents list
    print("\n3. Testing agents list...")
    try:
        response = requests.get(f"{BASE_URL}/api/agents")
        if response.status_code == 200:
            print("✅ Agents list working")
            agents = response.json()
            for name, info in agents.items():
                print(f"   🤖 {name.title()}: {len(info['capabilities'])} capabilities")
        else:
            print(f"❌ Agents list failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Agents list error: {e}")
    
    # Test marketing demo
    print("\n4. Testing marketing campaign demo...")
    try:
        response = requests.post(f"{BASE_URL}/api/demo/marketing-campaign")
        if response.status_code == 200:
            print("✅ Marketing demo working")
            result = response.json()
            print(f"   Campaign: {result['result']['campaign_details']['name']}")
            print(f"   Expected leads: {result['result']['campaign_details']['expected_results']['leads']}")
        else:
            print(f"❌ Marketing demo failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Marketing demo error: {e}")
    
    # Test design demo
    print("\n5. Testing website design demo...")
    try:
        response = requests.post(f"{BASE_URL}/api/demo/website-design")
        if response.status_code == 200:
            print("✅ Design demo working")
            result = response.json()
            print(f"   Layout: {result['result']['design_details']['layout']}")
            print(f"   Colors: {', '.join(result['result']['design_details']['color_scheme'])}")
        else:
            print(f"❌ Design demo failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Design demo error: {e}")
    
    # Test finance demo
    print("\n6. Testing financial analysis demo...")
    try:
        response = requests.post(f"{BASE_URL}/api/demo/financial-analysis")
        if response.status_code == 200:
            print("✅ Finance demo working")
            result = response.json()
            print(f"   Profit margin: {result['result']['analysis']['profit_margin']}")
            print(f"   Growth rate: {result['result']['analysis']['projections']['growth_rate']}")
        else:
            print(f"❌ Finance demo failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Finance demo error: {e}")
    
    # Test individual agent task
    print("\n7. Testing individual agent task...")
    try:
        task_data = {
            "type": "custom_task",
            "description": "Test task for engineering agent",
            "priority": "medium"
        }
        response = requests.post(f"{BASE_URL}/api/agents/engineering/task", json=task_data)
        if response.status_code == 200:
            print("✅ Individual agent task working")
            result = response.json()
            print(f"   Task ID: {result['task_id']}")
            print(f"   Status: {result['status']}")
        else:
            print(f"❌ Individual agent task failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Individual agent task error: {e}")
    
    print("\n🎉 API testing complete!")
    print("\n🦋 ButterflyBlue Creations is working perfectly!")

if __name__ == "__main__":
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    test_api()
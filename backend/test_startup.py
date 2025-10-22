#!/usr/bin/env python3
"""
Quick test to verify the app can start without errors.
Run this before deploying to catch startup issues.
"""

import sys
import os

print("=" * 50)
print("Testing app startup...")
print("=" * 50)

# Test 1: Check Python version
print(f"\n1. Python version: {sys.version}")

# Test 2: Check environment
print(f"\n2. PORT environment variable: {os.getenv('PORT', 'NOT SET')}")
print(f"   PYTHONUNBUFFERED: {os.getenv('PYTHONUNBUFFERED', 'NOT SET')}")

# Test 3: Try importing the app
print("\n3. Importing FastAPI app...")
try:
    from app.main import app
    print("   ✓ App imported successfully")
except Exception as e:
    print(f"   ✗ Failed to import app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Check routes
print("\n4. Checking routes...")
routes = [route.path for route in app.routes]
print(f"   Found {len(routes)} routes:")
for route in routes[:10]:  # Show first 10
    print(f"   - {route}")

# Test 5: Check health endpoint exists
print("\n5. Checking health endpoints...")
health_routes = [r for r in routes if 'health' in r.lower()]
if health_routes:
    print(f"   ✓ Found health endpoints: {health_routes}")
else:
    print("   ✗ No health endpoints found!")
    sys.exit(1)

print("\n" + "=" * 50)
print("All tests passed! App should start correctly.")
print("=" * 50)

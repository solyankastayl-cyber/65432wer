#!/usr/bin/env python3

"""
Backend API Testing for Fractal Platform
Tests all critical endpoints mentioned in the review request.
"""

import requests
import sys
from datetime import datetime
import json

class FractalAPITester:
    def __init__(self, base_url="https://fractal-index-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        
    def run_test(self, name, method, endpoint, expected_status=200, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            else:
                print(f"❌ Unsupported method: {method}")
                return False, {}
            
            print(f"   Status: {response.status_code}")
            
            # Handle both single status and list of acceptable statuses
            if isinstance(expected_status, list):
                success = response.status_code in expected_status
            else:
                success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, {"text": response.text[:200]}
            else:
                self.failed_tests.append({
                    "test": name,
                    "endpoint": endpoint,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "response": response.text[:500] if response.text else "No response body"
                })
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200] if response.text else 'No response'}")
                
            return False, {}
            
        except requests.exceptions.Timeout:
            print(f"❌ Failed - Timeout after {timeout}s")
            self.failed_tests.append({
                "test": name,
                "endpoint": endpoint,
                "error": f"Timeout after {timeout}s"
            })
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                "test": name,
                "endpoint": endpoint,
                "error": str(e)
            })
            return False, {}

    def test_health_endpoint(self):
        """Test backend health endpoint"""
        return self.run_test(
            "Backend Health Check",
            "GET",
            "/api/health"
        )

    def test_dxy_decision_api(self):
        """Test DXY fractal decision API"""
        return self.run_test(
            "DXY Decision API",
            "GET", 
            "/api/fractal/dxy/decision"
        )
        
    def test_dxy_overview_api(self):
        """Test DXY overview API for UI"""
        return self.run_test(
            "DXY Overview API",
            "GET",
            "/api/ui/fractal/dxy/overview?h=90"
        )

    def test_spx_fractal_api(self):
        """Test SPX fractal API"""
        return self.run_test(
            "SPX Fractal API",
            "GET",
            "/api/fractal/spx?focus=30d"
        )

    def test_btc_fractal_api(self):
        """Test BTC fractal API"""
        return self.run_test(
            "BTC Fractal API", 
            "GET",
            "/api/fractal/signal"
        )

    def test_admin_auth_endpoint(self):
        """Test admin auth endpoint"""
        return self.run_test(
            "Admin Auth Endpoint",
            "GET",
            "/api/admin/status",
            expected_status=[200, 401]  # Either OK or needs auth
        )

    def test_system_health(self):
        """Test system health endpoint"""
        return self.run_test(
            "System Health",
            "GET",
            "/api/system/health"
        )

    def test_fractal_match_api(self):
        """Test fractal match API"""
        return self.run_test(
            "Fractal Match API",
            "GET",
            "/api/fractal/match"
        )

    def test_macro_brain_api(self):
        """Test macro brain/brain API"""
        return self.run_test(
            "Brain API",
            "GET",
            "/api/brain/v2/status",
            expected_status=[200, 404]  # May not exist
        )

def main():
    print("═══════════════════════════════════════════════════════════════")
    print("  FRACTAL PLATFORM BACKEND API TESTING")
    print("═══════════════════════════════════════════════════════════════")
    
    tester = FractalAPITester()
    
    # Test critical endpoints mentioned in review request
    print("\n📋 Testing Core Endpoints...")
    
    # 1. Backend health endpoint /api/health
    tester.test_health_endpoint()
    
    # 2. System health 
    tester.test_system_health()
    
    # 3. DXY APIs
    tester.test_dxy_decision_api()
    tester.test_dxy_overview_api()
    
    # 4. SPX Fractal API
    tester.test_spx_fractal_api()
    
    # 5. BTC Fractal API
    tester.test_btc_fractal_api()
    
    # 6. Fractal match API
    tester.test_fractal_match_api()
    
    # 7. Admin panel API
    tester.test_admin_auth_endpoint()
    
    # 8. Brain/Macro API
    tester.test_macro_brain_api()
    
    # Print results summary
    print("\n═══════════════════════════════════════════════════════════════")
    print("  TEST RESULTS SUMMARY")
    print("═══════════════════════════════════════════════════════════════")
    
    success_rate = (tester.tests_passed / tester.tests_run) * 100 if tester.tests_run > 0 else 0
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run} ({success_rate:.1f}%)")
    
    if tester.failed_tests:
        print(f"\n❌ Failed tests ({len(tester.failed_tests)}):")
        for i, test in enumerate(tester.failed_tests, 1):
            print(f"  {i}. {test['test']}")
            print(f"     Endpoint: {test['endpoint']}")
            if 'expected' in test:
                print(f"     Expected: {test['expected']}, Got: {test['actual']}")
            if 'error' in test:
                print(f"     Error: {test['error']}")
            if 'response' in test:
                print(f"     Response: {test['response'][:150]}...")
    else:
        print("\n✅ All tests passed!")
    
    print(f"\n🕒 Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return appropriate exit code
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
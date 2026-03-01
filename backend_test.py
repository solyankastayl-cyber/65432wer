#!/usr/bin/env python3
"""
Fractal Index Platform - Backend API Testing
Tests all required endpoints for BTC, DXY, SPX, Brain, and system health
"""
import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class FractalAPITester:
    def __init__(self, base_url: str = "https://fractal-index-6.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session = requests.Session()
        self.session.timeout = 30

    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def run_test(self, name: str, method: str, endpoint: str, expected_status: int = 200, 
                 data: Optional[Dict] = None, headers: Optional[Dict] = None) -> tuple[bool, dict]:
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        self.log(f"Testing {name}... ({method} {url})")
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers)
            elif method == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = self.session.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                self.log(f"❌ Unsupported HTTP method: {method}", "ERROR")
                return False, {}

            # Check status code
            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                self.log(f"✅ {name} - Status: {response.status_code}")
                
                # Try to parse JSON response
                try:
                    json_response = response.json()
                    return True, json_response
                except:
                    return True, {"raw_response": response.text[:500]}
            else:
                error_info = {
                    "test": name,
                    "expected_status": expected_status,
                    "actual_status": response.status_code,
                    "response_text": response.text[:500]
                }
                self.failed_tests.append(error_info)
                self.log(f"❌ {name} - Expected {expected_status}, got {response.status_code}", "ERROR")
                self.log(f"   Response: {response.text[:200]}...", "ERROR")
                return False, error_info

        except requests.exceptions.Timeout:
            error_info = {"test": name, "error": "Request timeout"}
            self.failed_tests.append(error_info)
            self.log(f"❌ {name} - Timeout", "ERROR")
            return False, error_info
        except Exception as e:
            error_info = {"test": name, "error": str(e)}
            self.failed_tests.append(error_info)
            self.log(f"❌ {name} - Error: {str(e)}", "ERROR")
            return False, error_info

    def test_system_health(self):
        """Test general system health"""
        self.log("=== SYSTEM HEALTH TESTS ===")
        
        # 1. Main health endpoint
        success, response = self.run_test(
            "System Health Check", 
            "GET", 
            "/api/health"
        )
        
        if success and isinstance(response, dict):
            # Check for TypeScript backend status
            if "ts_backend" in response:
                ts_status = response["ts_backend"]
                if isinstance(ts_status, dict) and ts_status.get("ok"):
                    self.log("✅ TypeScript backend is healthy")
                else:
                    self.log(f"⚠️  TypeScript backend status: {ts_status}")
            
        return success

    def test_btc_fractal(self):
        """Test BTC Fractal API"""
        self.log("=== BTC FRACTAL TESTS ===")
        
        # 1. BTC Signal endpoint
        success1, response1 = self.run_test(
            "BTC Fractal Signal",
            "GET",
            "/api/fractal/signal"
        )
        
        if success1 and isinstance(response1, dict):
            if "signal" in response1:
                self.log(f"✅ BTC signal received: {response1.get('signal', 'Unknown')}")
            elif "action" in response1:
                self.log(f"✅ BTC action received: {response1.get('action', 'Unknown')}")
            else:
                self.log(f"⚠️  BTC response structure: {list(response1.keys())}")

        # 2. BTC Focus Pack (alternative endpoint)
        success2, response2 = self.run_test(
            "BTC Focus Pack",
            "GET",
            "/api/fractal/focus/BTC/90d",
            expected_status=200
        )

        return success1 and success2

    def test_dxy_fractal(self):
        """Test DXY Fractal API"""
        self.log("=== DXY FRACTAL TESTS ===")
        
        # 1. DXY UI Overview
        success1, response1 = self.run_test(
            "DXY Fractal Overview",
            "GET",
            "/api/ui/fractal/dxy/overview"
        )
        
        if success1 and isinstance(response1, dict):
            # Check for expected DXY data structure
            if "verdict" in response1:
                verdict = response1["verdict"]
                self.log(f"✅ DXY verdict: {verdict.get('bias', 'Unknown')} with {verdict.get('expectedMoveP50', 0)}% expected move")
            elif "data" in response1:
                self.log(f"✅ DXY data structure received")
            else:
                self.log(f"⚠️  DXY response structure: {list(response1.keys())}")

        # 2. DXY Fractal Signal (alternative)
        success2, response2 = self.run_test(
            "DXY Fractal Signal",
            "GET",
            "/api/fractal/dxy/signal",
            expected_status=200
        )

        return success1

    def test_spx_fractal(self):
        """Test SPX Fractal API"""
        self.log("=== SPX FRACTAL TESTS ===")
        
        # 1. SPX Fractal main endpoint
        success1, response1 = self.run_test(
            "SPX Fractal Data",
            "GET",
            "/api/fractal/spx"
        )
        
        if success1 and isinstance(response1, dict):
            # Check SPX data structure
            if "data" in response1:
                spx_data = response1["data"]
                if "decision" in spx_data:
                    decision = spx_data["decision"]
                    self.log(f"✅ SPX decision: {decision.get('action', 'Unknown')} with confidence {decision.get('confidence', 0)}")
                if "market" in spx_data:
                    market = spx_data["market"]
                    self.log(f"✅ SPX market phase: {market.get('phase', 'Unknown')}")
            else:
                self.log(f"⚠️  SPX response structure: {list(response1.keys())}")

        # 2. SPX Focus Pack
        success2, response2 = self.run_test(
            "SPX Focus Pack",
            "GET",
            "/api/fractal/focus/SPX/30d",
            expected_status=200
        )

        return success1

    def test_brain_status(self):
        """Test Brain/Macro Engine Status"""
        self.log("=== BRAIN/MACRO ENGINE TESTS ===")
        
        # 1. Brain v2 status
        success1, response1 = self.run_test(
            "Brain v2 Status",
            "GET",
            "/api/brain/v2/status"
        )
        
        if success1 and isinstance(response1, dict):
            self.log(f"✅ Brain status received: {response1.get('status', 'Unknown')}")
        
        # 2. UI Brain Overview (alternative)
        success2, response2 = self.run_test(
            "Brain UI Overview", 
            "GET",
            "/api/ui/brain/overview",
            expected_status=200
        )

        # 3. Macro Engine Health
        success3, response3 = self.run_test(
            "Macro Engine Health",
            "GET", 
            "/api/macro-engine/health",
            expected_status=200
        )

        return success1

    def test_admin_endpoints(self):
        """Test Admin Panel endpoints"""
        self.log("=== ADMIN PANEL TESTS ===")
        
        # 1. Admin auth status (should work without auth)
        success1, response1 = self.run_test(
            "Admin Auth Status",
            "GET",
            "/api/admin/auth/status",
            expected_status=200
        )

        return success1

    def test_additional_endpoints(self):
        """Test additional important endpoints"""
        self.log("=== ADDITIONAL ENDPOINTS ===")
        
        # 1. System health (alternative)
        success1, response1 = self.run_test(
            "System Health Alternative",
            "GET",
            "/api/system/health",
            expected_status=200
        )

        # 2. Index Engine V2
        success2, response2 = self.run_test(
            "Index Engine V2 - SPX Pack",
            "GET",
            "/api/v2/index/SPX/pack",
            expected_status=200
        )

        # 3. Fractal Engine Health
        success3, response3 = self.run_test(
            "Fractal Engine Health",
            "GET",
            "/api/fractal/health",
            expected_status=200
        )

        return True  # Non-critical tests

    def run_all_tests(self):
        """Run all API tests"""
        self.log("🚀 Starting Fractal Index Platform API Tests")
        self.log(f"Base URL: {self.base_url}")
        
        # Run test suites
        results = {
            "system_health": self.test_system_health(),
            "btc_fractal": self.test_btc_fractal(),
            "dxy_fractal": self.test_dxy_fractal(), 
            "spx_fractal": self.test_spx_fractal(),
            "brain_status": self.test_brain_status(),
            "admin_endpoints": self.test_admin_endpoints(),
            "additional": self.test_additional_endpoints()
        }
        
        # Print summary
        self.log("=" * 60)
        self.log("📊 TEST SUMMARY")
        self.log(f"Tests Run: {self.tests_run}")
        self.log(f"Tests Passed: {self.tests_passed}")
        self.log(f"Tests Failed: {len(self.failed_tests)}")
        self.log(f"Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%")
        
        # Print individual results
        for suite_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            self.log(f"{suite_name.upper()}: {status}")
        
        # Print failed tests details
        if self.failed_tests:
            self.log("=" * 60)
            self.log("❌ FAILED TESTS DETAILS:")
            for i, failure in enumerate(self.failed_tests, 1):
                self.log(f"{i}. {failure.get('test', 'Unknown')}")
                if 'expected_status' in failure:
                    self.log(f"   Expected: {failure['expected_status']}, Got: {failure['actual_status']}")
                if 'error' in failure:
                    self.log(f"   Error: {failure['error']}")
                if 'response_text' in failure:
                    self.log(f"   Response: {failure['response_text']}")
        
        # Return success if at least critical endpoints work
        critical_success = (
            results["system_health"] and 
            (results["btc_fractal"] or results["dxy_fractal"] or results["spx_fractal"])
        )
        
        return critical_success, results

def main():
    """Main test runner"""
    tester = FractalAPITester()
    
    try:
        success, results = tester.run_all_tests()
        
        # Exit with appropriate code
        exit_code = 0 if success else 1
        
        if success:
            tester.log("🎉 Critical endpoints are working! System is functional.")
        else:
            tester.log("💥 Critical endpoints failed! System needs attention.")
        
        return exit_code
        
    except KeyboardInterrupt:
        tester.log("🛑 Tests interrupted by user")
        return 1
    except Exception as e:
        tester.log(f"💥 Unexpected error: {e}", "ERROR")
        return 1

if __name__ == "__main__":
    sys.exit(main())
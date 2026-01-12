"""
Simple test script to verify crawler installations and basic functionality.
Run this to test your setup before using the Streamlit dashboard.
"""
import sys
import time

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        from crawlers import LightweightCrawler, BrowserCrawler, AICrawler
        from utils import AntiBot, BenchmarkEngine
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_lightweight_crawler():
    """Test the lightweight crawler."""
    print("\nTesting Lightweight Crawler...")
    try:
        from crawlers import LightweightCrawler
        
        crawler = LightweightCrawler()
        result = crawler.crawl("https://example.com")
        
        if result.success:
            print(f"✓ Lightweight crawler successful")
            print(f"  - Time: {result.time_taken:.2f}s")
            print(f"  - Status: {result.status_code}")
            print(f"  - Data size: {result.data_size} bytes")
            return True
        else:
            print(f"✗ Lightweight crawler failed: {result.error}")
            return False
    except Exception as e:
        print(f"✗ Lightweight crawler error: {e}")
        return False


def test_browser_crawler():
    """Test the browser-based crawler."""
    print("\nTesting Browser-Based Crawler...")
    try:
        from crawlers import BrowserCrawler
        
        print("  Note: This requires Playwright browsers to be installed.")
        print("  Run: playwright install chromium")
        
        crawler = BrowserCrawler()
        result = crawler.crawl("https://example.com")
        
        if result.success:
            print(f"✓ Browser crawler successful")
            print(f"  - Time: {result.time_taken:.2f}s")
            print(f"  - Status: {result.status_code}")
            print(f"  - Data size: {result.data_size} bytes")
            return True
        else:
            print(f"✗ Browser crawler failed: {result.error}")
            return False
    except Exception as e:
        print(f"✗ Browser crawler error: {e}")
        print("  Make sure to run: playwright install chromium")
        return False


def test_antibot():
    """Test anti-bot utilities."""
    print("\nTesting Anti-Bot Utilities...")
    try:
        from utils import AntiBot
        
        antibot = AntiBot()
        user_agent = antibot.get_random_user_agent()
        headers = antibot.get_headers()
        
        print(f"✓ Anti-bot utilities working")
        print(f"  - Generated user agent: {user_agent[:50]}...")
        print(f"  - Headers count: {len(headers)}")
        return True
    except Exception as e:
        print(f"✗ Anti-bot error: {e}")
        return False


def test_benchmark():
    """Test benchmarking engine."""
    print("\nTesting Benchmark Engine...")
    try:
        from utils import BenchmarkEngine
        from crawlers import LightweightCrawler
        
        engine = BenchmarkEngine()
        crawler = LightweightCrawler()
        
        # Run a simple crawl
        result = crawler.crawl("https://example.com")
        engine.add_result(result)
        
        # Get comparison table
        df = engine.get_comparison_table()
        
        if not df.empty:
            print(f"✓ Benchmark engine working")
            print(f"  - Results recorded: {len(df)}")
            return True
        else:
            print(f"✗ Benchmark engine failed to create comparison table")
            return False
    except Exception as e:
        print(f"✗ Benchmark error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Crawler-Duel Installation Test")
    print("=" * 60)
    
    results = []
    
    # Test imports first
    if not test_imports():
        print("\n❌ Basic imports failed. Please install requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Run other tests
    results.append(("Lightweight Crawler", test_lightweight_crawler()))
    results.append(("Browser Crawler", test_browser_crawler()))
    results.append(("Anti-Bot Utilities", test_antibot()))
    results.append(("Benchmark Engine", test_benchmark()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! You're ready to use Crawler-Duel.")
        print("   Run: streamlit run app.py")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

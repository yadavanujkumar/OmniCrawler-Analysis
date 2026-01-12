"""
Simple example showing how to use Crawler-Duel programmatically.
"""
from crawlers import LightweightCrawler, BrowserCrawler
from utils import AntiBot, BenchmarkEngine


def main():
    print("Crawler-Duel - Programmatic Example")
    print("=" * 50)
    
    # Target URL
    url = "https://example.com"
    print(f"\nTarget URL: {url}")
    
    # Initialize components
    engine = BenchmarkEngine()
    antibot = AntiBot()
    
    # Test Lightweight Crawler
    print("\n1. Testing Lightweight Crawler...")
    lightweight = LightweightCrawler(timeout=15)
    
    try:
        result = lightweight.crawl(
            url,
            user_agent=antibot.get_random_user_agent()
        )
        
        print(f"   Success: {result.success}")
        print(f"   Time: {result.time_taken:.2f}s")
        print(f"   Status: {result.status_code}")
        print(f"   Size: {result.data_size} bytes")
        
        if result.success:
            engine.add_result(result)
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test Browser Crawler
    print("\n2. Testing Browser-Based Crawler...")
    browser = BrowserCrawler(headless=True, timeout=15000)
    
    try:
        result = browser.crawl(
            url,
            user_agent=antibot.get_random_user_agent()
        )
        
        print(f"   Success: {result.success}")
        print(f"   Time: {result.time_taken:.2f}s")
        print(f"   Status: {result.status_code}")
        print(f"   Size: {result.data_size} bytes")
        
        if result.success:
            engine.add_result(result)
    except Exception as e:
        print(f"   Error: {e}")
    
    # Show results if any crawls succeeded
    if len(engine.results) > 0:
        print("\n" + "=" * 50)
        print("RESULTS")
        print("=" * 50)
        
        # Winner
        winner = engine.get_winner()
        if winner['winner']:
            print(f"\n🏆 Winner: {winner['winner']}")
            print(f"   {winner['reason']}")
        
        # Comparison table
        print("\n📊 Comparison Table:")
        comparison = engine.get_comparison_table()
        print(comparison.to_string(index=False))
        
        # Cost-benefit
        print("\n💰 Cost-Benefit Analysis:")
        cb_analysis = engine.get_cost_benefit_analysis()
        print(cb_analysis.to_string(index=False))
    else:
        print("\n⚠️  No successful crawls. This may be due to network restrictions.")
        print("   Try running the demo.py script to see functionality with mock data.")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()

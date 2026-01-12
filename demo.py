"""
Demo script showing Crawler-Duel functionality without external network access.
This creates mock results to demonstrate the benchmarking system.
"""
from crawlers import CrawlResult
from utils import BenchmarkEngine, AntiBot
import time


def create_mock_result(crawler_type: str, url: str, success: bool = True, 
                       time_taken: float = 1.0, data_size: int = 5000,
                       status_code: int = 200) -> CrawlResult:
    """Create a mock crawl result for demonstration."""
    content = "<html><body>Mock content</body></html>" if success else None
    
    metadata = {
        'has_json': crawler_type == 'AI-Agentic',
        'has_markdown': crawler_type == 'AI-Agentic',
        'clean_text': crawler_type in ['AI-Agentic', 'Browser-Based'],
        'raw_html': content
    }
    
    return CrawlResult(
        url=url,
        success=success,
        time_taken=time_taken,
        status_code=status_code if success else None,
        content=content,
        error=None if success else "Mock error",
        data_size=data_size if success else 0,
        crawler_type=crawler_type,
        metadata=metadata
    )


def demo_benchmark_engine():
    """Demonstrate the benchmark engine with mock results."""
    print("=" * 70)
    print("Crawler-Duel Demo - Benchmarking Engine")
    print("=" * 70)
    print()
    
    # Create benchmark engine
    engine = BenchmarkEngine()
    
    # Simulate a race with three crawlers
    print("🏁 Simulating a race between three crawlers...")
    print()
    
    # Lightweight crawler - fast but basic
    print("1️⃣  Lightweight Crawler: Fast HTTP request...")
    result1 = create_mock_result(
        crawler_type="Lightweight",
        url="https://example.com",
        success=True,
        time_taken=0.5,
        data_size=8000,
        status_code=200
    )
    engine.add_result(result1)
    print(f"   ✓ Completed in {result1.time_taken}s")
    time.sleep(0.3)
    
    # Browser crawler - slower but handles JS
    print("2️⃣  Browser-Based Crawler: Running Playwright...")
    result2 = create_mock_result(
        crawler_type="Browser-Based",
        url="https://example.com",
        success=True,
        time_taken=2.3,
        data_size=12000,
        status_code=200
    )
    engine.add_result(result2)
    print(f"   ✓ Completed in {result2.time_taken}s")
    time.sleep(0.3)
    
    # AI crawler - slowest but best quality
    print("3️⃣  AI-Agentic Crawler: Using Firecrawl API...")
    result3 = create_mock_result(
        crawler_type="AI-Agentic",
        url="https://example.com",
        success=True,
        time_taken=3.5,
        data_size=6000,
        status_code=200
    )
    engine.add_result(result3)
    print(f"   ✓ Completed in {result3.time_taken}s")
    print()
    
    # Show winner
    print("-" * 70)
    winner_info = engine.get_winner()
    print(f"🏆 Winner: {winner_info['winner']}")
    print(f"   {winner_info['reason']}")
    print()
    
    # Show all scores
    print("📊 Detailed Scores:")
    for crawler, score in winner_info['all_scores'].items():
        print(f"   {crawler}: {score:.1f}/100")
    print()
    
    # Show comparison table
    print("-" * 70)
    print("📊 Comparison Table:")
    print("-" * 70)
    comparison_df = engine.get_comparison_table()
    print(comparison_df.to_string(index=False))
    print()
    
    # Show cost-benefit analysis
    print("-" * 70)
    print("💰 Cost-Benefit Analysis:")
    print("-" * 70)
    cb_df = engine.get_cost_benefit_analysis()
    print(cb_df.to_string(index=False))
    print()
    
    # Show summary stats
    print("-" * 70)
    print("📈 Summary Statistics:")
    print("-" * 70)
    stats = engine.get_summary_stats()
    print(f"   Total Crawls: {stats['total_crawls']}")
    print(f"   Successful: {stats['successful_crawls']}")
    print(f"   Average Time: {stats['avg_time']:.2f}s")
    print(f"   Total Data: {stats['total_data_size'] / 1024:.1f} KB")
    print(f"   Crawlers Tested: {', '.join(stats['crawlers_tested'])}")
    print()


def demo_antibot():
    """Demonstrate anti-bot utilities."""
    print("=" * 70)
    print("Anti-Bot Utilities Demo")
    print("=" * 70)
    print()
    
    # Create anti-bot instance
    antibot = AntiBot()
    
    print("🛡️  User-Agent Randomization:")
    for i in range(3):
        ua = antibot.get_random_user_agent()
        print(f"   {i+1}. {ua}")
    print()
    
    print("🔄 HTTP Headers Generation:")
    headers = antibot.get_headers()
    for key, value in list(headers.items())[:5]:
        print(f"   {key}: {value}")
    print(f"   ... and {len(headers) - 5} more headers")
    print()
    
    # Demo with proxies
    proxies = ['http://proxy1.example.com:8080', 'http://proxy2.example.com:8080']
    antibot_with_proxy = AntiBot(proxies=proxies)
    
    print("🔄 Proxy Rotation:")
    for i in range(3):
        proxy = antibot_with_proxy.get_next_proxy()
        print(f"   Request {i+1}: {proxy['http']}")
    print()


def demo_quality_scores():
    """Demonstrate quality scoring system."""
    print("=" * 70)
    print("Structural Quality Scoring Demo")
    print("=" * 70)
    print()
    
    # Different types of results
    print("Quality scores (0-100) for different crawler outputs:")
    print()
    
    # Raw HTML (lowest quality)
    html_result = create_mock_result(
        crawler_type="Lightweight",
        url="https://example.com",
        success=True
    )
    html_result.metadata = {'has_json': False, 'has_markdown': False, 'clean_text': False}
    print(f"   Raw HTML output: {html_result.get_structural_quality_score():.1f}/100")
    
    # Browser with clean text
    browser_result = create_mock_result(
        crawler_type="Browser-Based",
        url="https://example.com",
        success=True
    )
    browser_result.metadata = {'has_json': False, 'has_markdown': False, 'clean_text': True}
    print(f"   Clean text extraction: {browser_result.get_structural_quality_score():.1f}/100")
    
    # AI with markdown
    ai_markdown = create_mock_result(
        crawler_type="AI-Agentic",
        url="https://example.com",
        success=True
    )
    ai_markdown.metadata = {'has_json': False, 'has_markdown': True, 'clean_text': True}
    print(f"   Markdown format: {ai_markdown.get_structural_quality_score():.1f}/100")
    
    # AI with JSON (highest quality)
    ai_json = create_mock_result(
        crawler_type="AI-Agentic",
        url="https://example.com",
        success=True
    )
    ai_json.metadata = {'has_json': True, 'has_markdown': True, 'clean_text': True}
    print(f"   Structured JSON: {ai_json.get_structural_quality_score():.1f}/100")
    print()


def main():
    """Run all demos."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "🕷️  Crawler-Duel Demo 🕷️" + " " * 22 + "║")
    print("║" + " " * 13 + "Multi-Agent Web Crawling & Benchmarking" + " " * 14 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Run demos
    demo_benchmark_engine()
    print()
    demo_antibot()
    print()
    demo_quality_scores()
    
    print("=" * 70)
    print("🎉 Demo Complete!")
    print()
    print("To run the full Streamlit dashboard, use:")
    print("   streamlit run app.py")
    print()
    print("For production use with real websites, you'll need:")
    print("   1. Network access to target URLs")
    print("   2. Playwright browsers installed: playwright install chromium")
    print("   3. (Optional) Firecrawl API key for AI-Agentic crawler")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()

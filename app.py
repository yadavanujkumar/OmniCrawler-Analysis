"""
Crawler-Duel: Multi-Agent Web Crawling & Benchmarking Suite
Streamlit Dashboard for live crawler racing and comparison.
"""
import streamlit as st
import time
from threading import Thread
from queue import Queue
import os
from dotenv import load_dotenv

from crawlers import LightweightCrawler, BrowserCrawler, AICrawler
from utils import AntiBot, BenchmarkEngine

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Crawler-Duel 🕷️",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .crawler-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #ddd;
        margin: 0.5rem 0;
    }
    .success {
        background-color: #d4edda;
        border-color: #28a745;
    }
    .failure {
        background-color: #f8d7da;
        border-color: #dc3545;
    }
    .running {
        background-color: #fff3cd;
        border-color: #ffc107;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'benchmark_engine' not in st.session_state:
        st.session_state.benchmark_engine = BenchmarkEngine()
    if 'antibot' not in st.session_state:
        st.session_state.antibot = AntiBot()
    if 'crawl_results' not in st.session_state:
        st.session_state.crawl_results = {}
    if 'race_complete' not in st.session_state:
        st.session_state.race_complete = False


def run_crawler_with_antibot(crawler, url, antibot, result_queue, crawler_name):
    """Run a crawler with anti-bot features and put result in queue."""
    try:
        user_agent = antibot.get_random_user_agent()
        proxy = antibot.get_random_proxy()
        
        result = crawler.crawl(url, user_agent=user_agent, proxy=proxy)
        result_queue.put((crawler_name, result))
    except Exception as e:
        result_queue.put((crawler_name, None))


def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🕷️ Crawler-Duel 🕷️</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem;">Multi-Agent Web Crawling & Benchmarking Suite</p>', unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # URL input
    url = st.sidebar.text_input(
        "Target URL",
        value="https://example.com",
        help="Enter the URL you want to crawl"
    )
    
    # Crawler selection
    st.sidebar.subheader("Select Crawlers")
    use_lightweight = st.sidebar.checkbox("Lightweight (HTTP)", value=True)
    use_browser = st.sidebar.checkbox("Browser-Based (Playwright)", value=True)
    use_ai = st.sidebar.checkbox("AI-Agentic (Firecrawl)", value=False, 
                                   help="Requires FIRECRAWL_API_KEY in .env file")
    
    # Anti-bot configuration
    st.sidebar.subheader("🛡️ Anti-Bot Settings")
    use_antibot = st.sidebar.checkbox("Enable Anti-Bot Features", value=True)
    
    # Proxy configuration
    proxy_input = st.sidebar.text_area(
        "Proxies (one per line)",
        help="Format: http://proxy:port",
        height=100
    )
    
    # API Key for AI crawler
    if use_ai:
        api_key = st.sidebar.text_input(
            "Firecrawl API Key",
            type="password",
            value=os.getenv('FIRECRAWL_API_KEY', ''),
            help="Required for AI-Agentic crawler"
        )
    else:
        api_key = None
    
    # Start race button
    start_race = st.sidebar.button("🏁 Start Race", type="primary", use_container_width=True)
    
    # Main content area
    if start_race and url:
        st.session_state.race_complete = False
        st.session_state.crawl_results = {}
        st.session_state.benchmark_engine.clear_results()
        
        # Parse proxies
        proxies = []
        if proxy_input.strip():
            proxies = [p.strip() for p in proxy_input.split('\n') if p.strip()]
        
        # Initialize anti-bot
        antibot = AntiBot(proxies=proxies if proxies else None)
        
        # Prepare crawlers
        crawlers_to_run = []
        
        if use_lightweight:
            crawlers_to_run.append(('Lightweight', LightweightCrawler()))
        if use_browser:
            crawlers_to_run.append(('Browser-Based', BrowserCrawler()))
        if use_ai and api_key:
            crawlers_to_run.append(('AI-Agentic', AICrawler(api_key=api_key)))
        
        if not crawlers_to_run:
            st.error("❌ Please select at least one crawler!")
            return
        
        # Create columns for live race display
        st.subheader("🏁 Live Race Progress")
        cols = st.columns(len(crawlers_to_run))
        
        # Create placeholders for each crawler
        placeholders = {}
        for idx, (name, _) in enumerate(crawlers_to_run):
            with cols[idx]:
                placeholders[name] = {
                    'status': st.empty(),
                    'time': st.empty(),
                    'result': st.empty()
                }
                placeholders[name]['status'].markdown(f"**{name}**")
                placeholders[name]['time'].info("⏳ Waiting to start...")
        
        # Run crawlers in parallel
        result_queue = Queue()
        threads = []
        
        st.info(f"🚀 Racing {len(crawlers_to_run)} crawler(s) against **{url}**")
        
        # Start all crawlers
        for name, crawler in crawlers_to_run:
            placeholders[name]['time'].warning(f"🏃 Running...")
            thread = Thread(
                target=run_crawler_with_antibot,
                args=(crawler, url, antibot if use_antibot else AntiBot(), result_queue, name)
            )
            thread.start()
            threads.append(thread)
        
        # Collect results as they complete
        results_received = 0
        while results_received < len(crawlers_to_run):
            if not result_queue.empty():
                crawler_name, result = result_queue.get()
                results_received += 1
                
                if result:
                    st.session_state.crawl_results[crawler_name] = result
                    st.session_state.benchmark_engine.add_result(result)
                    
                    # Update display
                    if result.success:
                        placeholders[crawler_name]['time'].success(
                            f"✅ Completed in {result.time_taken:.2f}s"
                        )
                        placeholders[crawler_name]['result'].markdown(
                            f"📊 Data: {result.data_size / 1024:.1f} KB | Status: {result.status_code}"
                        )
                    else:
                        placeholders[crawler_name]['time'].error(
                            f"❌ Failed after {result.time_taken:.2f}s"
                        )
                        placeholders[crawler_name]['result'].markdown(
                            f"⚠️ Error: {result.error}"
                        )
                else:
                    placeholders[crawler_name]['time'].error("❌ Failed")
            
            time.sleep(0.1)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        st.session_state.race_complete = True
        st.success("🏁 Race Complete!")
    
    # Display results if race is complete
    if st.session_state.race_complete and st.session_state.crawl_results:
        st.markdown("---")
        
        # Winner announcement
        st.subheader("🏆 Race Results")
        winner_info = st.session_state.benchmark_engine.get_winner()
        
        if winner_info['winner']:
            st.success(f"🥇 **Winner: {winner_info['winner']}**")
            st.info(winner_info['reason'])
            
            # Show all scores
            with st.expander("📊 Detailed Scores"):
                for crawler, score in winner_info['all_scores'].items():
                    st.write(f"**{crawler}**: {score:.1f}/100")
        
        # Comparison table
        st.subheader("📊 Comparison Table")
        comparison_df = st.session_state.benchmark_engine.get_comparison_table()
        st.dataframe(comparison_df, use_container_width=True)
        
        # Cost-benefit analysis
        st.subheader("💰 Cost-Benefit Analysis")
        cb_df = st.session_state.benchmark_engine.get_cost_benefit_analysis()
        st.dataframe(cb_df, use_container_width=True)
        
        st.markdown("""
        **Legend:**
        - **Relative Cost**: Resource consumption (1=lowest, 10=highest)
        - **Benefit Score**: Overall value considering success, integrity, and quality
        - **Cost-Benefit Ratio**: Higher is better
        - **Recommendation**: Overall assessment
        """)
        
        # Summary statistics
        with st.expander("📈 Summary Statistics"):
            stats = st.session_state.benchmark_engine.get_summary_stats()
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Crawls", stats.get('total_crawls', 0))
            with col2:
                st.metric("Successful", stats.get('successful_crawls', 0))
            with col3:
                st.metric("Avg Time", f"{stats.get('avg_time', 0):.2f}s")
            with col4:
                st.metric("Total Data", f"{stats.get('total_data_size', 0) / 1024:.1f} KB")
        
        # Detailed results
        with st.expander("🔍 Detailed Results"):
            for crawler_name, result in st.session_state.crawl_results.items():
                st.markdown(f"### {crawler_name}")
                st.json({
                    'URL': result.url,
                    'Success': result.success,
                    'Time Taken': f"{result.time_taken:.3f}s",
                    'Status Code': result.status_code,
                    'Data Size': f"{result.data_size} bytes",
                    'Has Data Integrity Issues': result.has_data_integrity_issues(),
                    'Structural Quality Score': f"{result.get_structural_quality_score():.1f}/100",
                    'Error': result.error if result.error else None
                })
    
    # Information section
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.markdown("""
    **Crawler-Duel** benchmarks three types of web crawlers:
    
    1. **Lightweight**: Fast HTTP requests
    2. **Browser-Based**: Playwright automation
    3. **AI-Agentic**: LLM-powered extraction
    
    Features:
    - Live race visualization
    - Performance metrics
    - Data integrity checks
    - Cost-benefit analysis
    - Anti-bot capabilities
    """)


if __name__ == "__main__":
    main()

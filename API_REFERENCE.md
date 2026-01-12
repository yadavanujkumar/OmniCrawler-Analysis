# Crawler-Duel API Reference

## Core Modules

### crawlers.base_crawler

#### `CrawlResult`
Data class representing the result of a crawl operation.

**Attributes:**
- `url` (str): The URL that was crawled
- `success` (bool): Whether the crawl was successful
- `time_taken` (float): Time in seconds to complete the crawl
- `status_code` (Optional[int]): HTTP status code
- `content` (Optional[str]): The crawled content
- `error` (Optional[str]): Error message if failed
- `data_size` (int): Size of content in bytes
- `crawler_type` (str): Name of the crawler used
- `metadata` (Dict[str, Any]): Additional crawler-specific data

**Methods:**
- `has_data_integrity_issues() -> bool`: Check for data problems
- `get_structural_quality_score() -> float`: Get quality score (0-100)

#### `BaseCrawler`
Abstract base class for all crawlers.

**Methods:**
- `crawl(url: str, **kwargs) -> CrawlResult`: Crawl a URL (abstract)

---

### crawlers.lightweight_crawler

#### `LightweightCrawler`
Fast HTTP-based crawler using requests library.

**Constructor:**
```python
LightweightCrawler(timeout: int = 30)
```

**Parameters:**
- `timeout`: Request timeout in seconds

**Methods:**
```python
crawl(url: str, 
      user_agent: Optional[str] = None,
      proxy: Optional[dict] = None, 
      **kwargs) -> CrawlResult
```

**Example:**
```python
from crawlers import LightweightCrawler

crawler = LightweightCrawler(timeout=15)
result = crawler.crawl("https://example.com")

if result.success:
    print(f"Fetched {result.data_size} bytes in {result.time_taken:.2f}s")
```

---

### crawlers.browser_crawler

#### `BrowserCrawler`
Browser-based crawler using Playwright for JavaScript execution.

**Constructor:**
```python
BrowserCrawler(headless: bool = True, timeout: int = 30000)
```

**Parameters:**
- `headless`: Run browser in headless mode
- `timeout`: Page load timeout in milliseconds

**Methods:**
```python
crawl(url: str,
      user_agent: Optional[str] = None,
      proxy: Optional[dict] = None,
      **kwargs) -> CrawlResult
```

**Example:**
```python
from crawlers import BrowserCrawler

crawler = BrowserCrawler(headless=True)
result = crawler.crawl("https://example.com")

if result.success:
    print(f"Title: {result.metadata.get('title')}")
```

---

### crawlers.ai_crawler

#### `AICrawler`
AI-powered crawler using Firecrawl or Crawl4AI for structured extraction.

**Constructor:**
```python
AICrawler(api_key: Optional[str] = None, use_firecrawl: bool = True)
```

**Parameters:**
- `api_key`: Firecrawl API key (or from FIRECRAWL_API_KEY env var)
- `use_firecrawl`: Use Firecrawl if True, otherwise Crawl4AI

**Methods:**
```python
crawl(url: str, **kwargs) -> CrawlResult
```

**Example:**
```python
from crawlers import AICrawler
import os

crawler = AICrawler(api_key=os.getenv('FIRECRAWL_API_KEY'))
result = crawler.crawl("https://example.com")

if result.success:
    markdown = result.metadata.get('markdown')
    print(markdown)
```

---

### utils.antibot

#### `AntiBot`
Utilities for bypassing anti-bot measures.

**Constructor:**
```python
AntiBot(proxies: Optional[List[str]] = None,
        custom_user_agents: Optional[List[str]] = None)
```

**Parameters:**
- `proxies`: List of proxy URLs
- `custom_user_agents`: List of custom user agent strings

**Methods:**
```python
get_random_user_agent() -> str
get_next_proxy() -> Optional[Dict[str, str]]
get_random_proxy() -> Optional[Dict[str, str]]
get_headers() -> Dict[str, str]
```

**Example:**
```python
from utils import AntiBot

# Without proxies
antibot = AntiBot()
ua = antibot.get_random_user_agent()
headers = antibot.get_headers()

# With proxies
proxies = ['http://proxy1:8080', 'http://proxy2:8080']
antibot = AntiBot(proxies=proxies)
proxy = antibot.get_next_proxy()
```

---

### utils.benchmark

#### `BenchmarkEngine`
Engine for benchmarking and comparing crawler results.

**Constructor:**
```python
BenchmarkEngine()
```

**Methods:**
```python
add_result(result: CrawlResult) -> None
clear_results() -> None
get_comparison_table() -> pd.DataFrame
get_winner() -> Dict[str, Any]
get_cost_benefit_analysis() -> pd.DataFrame
get_summary_stats() -> Dict[str, Any]
```

**Example:**
```python
from utils import BenchmarkEngine
from crawlers import LightweightCrawler

engine = BenchmarkEngine()

crawler = LightweightCrawler()
result = crawler.crawl("https://example.com")
engine.add_result(result)

# Get comparison
df = engine.get_comparison_table()
print(df)

# Get winner
winner = engine.get_winner()
print(f"Winner: {winner['winner']}")
```

---

## Complete Usage Example

```python
from crawlers import LightweightCrawler, BrowserCrawler, AICrawler
from utils import AntiBot, BenchmarkEngine
import os

# Initialize
url = "https://example.com"
engine = BenchmarkEngine()
antibot = AntiBot()

# Create crawlers
crawlers = [
    ('Lightweight', LightweightCrawler()),
    ('Browser', BrowserCrawler()),
    ('AI', AICrawler(api_key=os.getenv('FIRECRAWL_API_KEY')))
]

# Run race
for name, crawler in crawlers:
    ua = antibot.get_random_user_agent()
    result = crawler.crawl(url, user_agent=ua)
    engine.add_result(result)
    print(f"{name}: {result.time_taken:.2f}s")

# Get results
winner = engine.get_winner()
print(f"\nWinner: {winner['winner']}")
print(winner['reason'])

comparison = engine.get_comparison_table()
print("\n", comparison)

cb_analysis = engine.get_cost_benefit_analysis()
print("\n", cb_analysis)
```

---

## Environment Variables

- `FIRECRAWL_API_KEY`: API key for Firecrawl service
- `HTTP_PROXY`: HTTP proxy URL
- `HTTPS_PROXY`: HTTPS proxy URL
- `CUSTOM_USER_AGENTS`: Comma-separated list of user agents

---

## Return Values

### CrawlResult Metadata Structure

**Lightweight Crawler:**
```python
{
    'raw_html': str,
    'text_content': str,
    'has_json': False,
    'has_markdown': False,
    'clean_text': False,
    'headers': dict,
    'redirects': int
}
```

**Browser Crawler:**
```python
{
    'raw_html': str,
    'text_content': str,
    'title': str,
    'has_json': False,
    'has_markdown': False,
    'clean_text': False,
    'url_after_redirects': str
}
```

**AI Crawler (Firecrawl):**
```python
{
    'markdown': str,
    'html': str,
    'metadata': dict,
    'has_json': True,
    'has_markdown': True,
    'clean_text': True
}
```

### Winner Dictionary Structure

```python
{
    'winner': str,           # Name of winning crawler
    'score': float,          # Score (0-100)
    'reason': str,           # Human-readable explanation
    'all_scores': dict       # All crawler scores
}
```

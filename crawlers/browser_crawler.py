"""
Browser-based crawler using Playwright.
Handles JavaScript-heavy sites with high fidelity.
"""
import time
from typing import Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from .base_crawler import BaseCrawler, CrawlResult


class BrowserCrawler(BaseCrawler):
    """Browser-based crawler using Playwright."""
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        super().__init__("Browser-Based")
        self.headless = headless
        self.timeout = timeout
    
    def crawl(self, url: str, user_agent: Optional[str] = None, proxy: Optional[dict] = None, **kwargs) -> CrawlResult:
        """
        Crawl a URL using Playwright browser automation.
        
        Args:
            url: The URL to crawl
            user_agent: Optional custom user agent
            proxy: Optional proxy configuration
            **kwargs: Additional parameters
            
        Returns:
            CrawlResult object
        """
        start_time = time.time()
        
        try:
            with sync_playwright() as p:
                # Launch browser with options
                browser_args = {
                    'headless': self.headless,
                }
                
                if proxy:
                    browser_args['proxy'] = {
                        'server': proxy.get('http', proxy.get('https', '')),
                    }
                
                browser = p.chromium.launch(**browser_args)
                
                # Create context with user agent
                context_args = {}
                if user_agent:
                    context_args['user_agent'] = user_agent
                
                context = browser.new_context(**context_args)
                page = context.new_page()
                
                # Set timeout
                page.set_default_timeout(self.timeout)
                
                # Navigate to URL
                response = page.goto(url, wait_until='networkidle')
                
                # Get content after JavaScript execution
                content = page.content()
                
                # Extract text content
                text_content = page.evaluate('() => document.body.innerText')
                
                # Get status code
                status_code = response.status if response else None
                
                # Check for blocking indicators
                title = page.title()
                
                metadata = {
                    'raw_html': content,
                    'text_content': text_content,
                    'title': title,
                    'has_json': False,
                    'has_markdown': False,
                    'clean_text': False,
                    'url_after_redirects': page.url
                }
                
                browser.close()
                
                return self._create_result(
                    url=url,
                    success=status_code == 200 if status_code else False,
                    start_time=start_time,
                    status_code=status_code,
                    content=content,
                    metadata=metadata
                )
                
        except PlaywrightTimeout:
            return self._create_result(
                url=url,
                success=False,
                start_time=start_time,
                error="Browser timeout",
                metadata={}
            )
        except Exception as e:
            return self._create_result(
                url=url,
                success=False,
                start_time=start_time,
                error=f"Browser error: {str(e)}",
                metadata={}
            )

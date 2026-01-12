"""
AI-Agentic crawler using Firecrawl or Crawl4AI.
Uses LLMs to extract clean Markdown/JSON from web pages.
"""
import time
import os
from typing import Optional
from .base_crawler import BaseCrawler, CrawlResult


class AICrawler(BaseCrawler):
    """AI-powered crawler using Firecrawl or Crawl4AI."""
    
    def __init__(self, api_key: Optional[str] = None, use_firecrawl: bool = True):
        super().__init__("AI-Agentic")
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        self.use_firecrawl = use_firecrawl
    
    def crawl(self, url: str, **kwargs) -> CrawlResult:
        """
        Crawl a URL using AI-powered extraction.
        
        Args:
            url: The URL to crawl
            **kwargs: Additional parameters
            
        Returns:
            CrawlResult object
        """
        start_time = time.time()
        
        if self.use_firecrawl:
            return self._crawl_with_firecrawl(url, start_time)
        else:
            return self._crawl_with_crawl4ai(url, start_time)
    
    def _crawl_with_firecrawl(self, url: str, start_time: float) -> CrawlResult:
        """Crawl using Firecrawl API."""
        try:
            from firecrawl import FirecrawlApp
            
            if not self.api_key:
                return self._create_result(
                    url=url,
                    success=False,
                    start_time=start_time,
                    error="Firecrawl API key not provided",
                    metadata={}
                )
            
            app = FirecrawlApp(api_key=self.api_key)
            
            # Scrape with markdown format
            result = app.scrape_url(url, params={'formats': ['markdown', 'html']})
            
            if result and 'markdown' in result:
                metadata = {
                    'markdown': result.get('markdown', ''),
                    'html': result.get('html', ''),
                    'metadata': result.get('metadata', {}),
                    'has_json': True,
                    'has_markdown': True,
                    'clean_text': True
                }
                
                content = result.get('markdown', result.get('html', ''))
                
                return self._create_result(
                    url=url,
                    success=True,
                    start_time=start_time,
                    status_code=200,
                    content=content,
                    metadata=metadata
                )
            else:
                return self._create_result(
                    url=url,
                    success=False,
                    start_time=start_time,
                    error="No data returned from Firecrawl",
                    metadata={}
                )
                
        except ImportError:
            return self._create_result(
                url=url,
                success=False,
                start_time=start_time,
                error="Firecrawl library not installed. Run: pip install firecrawl-py",
                metadata={}
            )
        except Exception as e:
            return self._create_result(
                url=url,
                success=False,
                start_time=start_time,
                error=f"Firecrawl error: {str(e)}",
                metadata={}
            )
    
    def _crawl_with_crawl4ai(self, url: str, start_time: float) -> CrawlResult:
        """Crawl using Crawl4AI library."""
        try:
            from crawl4ai import WebCrawler
            
            crawler = WebCrawler()
            crawler.warmup()
            
            result = crawler.run(url)
            
            if result.success:
                metadata = {
                    'markdown': result.markdown,
                    'cleaned_html': result.cleaned_html,
                    'media': result.media,
                    'links': result.links,
                    'has_json': False,
                    'has_markdown': True,
                    'clean_text': True
                }
                
                return self._create_result(
                    url=url,
                    success=True,
                    start_time=start_time,
                    status_code=200,
                    content=result.markdown,
                    metadata=metadata
                )
            else:
                return self._create_result(
                    url=url,
                    success=False,
                    start_time=start_time,
                    error=result.error_message,
                    metadata={}
                )
                
        except ImportError:
            return self._create_result(
                url=url,
                success=False,
                start_time=start_time,
                error="Crawl4AI library not installed. Run: pip install crawl4ai",
                metadata={}
            )
        except Exception as e:
            return self._create_result(
                url=url,
                success=False,
                start_time=start_time,
                error=f"Crawl4AI error: {str(e)}",
                metadata={}
            )

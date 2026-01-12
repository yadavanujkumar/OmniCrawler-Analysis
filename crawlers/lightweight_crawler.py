"""
Lightweight HTTP-based crawler using requests library.
Fast and low-resource implementation.
"""
import requests
from bs4 import BeautifulSoup
import time
from typing import Optional
from .base_crawler import BaseCrawler, CrawlResult


class LightweightCrawler(BaseCrawler):
    """Lightweight crawler using simple HTTP requests."""
    
    def __init__(self, timeout: int = 30):
        super().__init__("Lightweight")
        self.timeout = timeout
        self.session = requests.Session()
    
    def crawl(self, url: str, user_agent: Optional[str] = None, proxy: Optional[dict] = None, **kwargs) -> CrawlResult:
        """
        Crawl a URL using simple HTTP requests.
        
        Args:
            url: The URL to crawl
            user_agent: Optional custom user agent
            proxy: Optional proxy configuration
            **kwargs: Additional parameters
            
        Returns:
            CrawlResult object
        """
        start_time = time.time()
        
        # Set headers
        headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.timeout,
                proxies=proxy,
                allow_redirects=True
            )
            
            # Parse with BeautifulSoup for basic extraction
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract text content
            for script in soup(["script", "style"]):
                script.decompose()
            text_content = soup.get_text(separator='\n', strip=True)
            
            metadata = {
                'raw_html': response.text,
                'text_content': text_content,
                'has_json': False,
                'has_markdown': False,
                'clean_text': False,
                'headers': dict(response.headers),
                'redirects': len(response.history)
            }
            
            return self._create_result(
                url=url,
                success=response.status_code == 200,
                start_time=start_time,
                status_code=response.status_code,
                content=response.text,
                metadata=metadata
            )
            
        except requests.exceptions.Timeout:
            return self._create_result(
                url=url,
                success=False,
                start_time=start_time,
                error="Request timeout",
                metadata={}
            )
        except requests.exceptions.ConnectionError as e:
            return self._create_result(
                url=url,
                success=False,
                start_time=start_time,
                error=f"Connection error: {str(e)}",
                metadata={}
            )
        except Exception as e:
            return self._create_result(
                url=url,
                success=False,
                start_time=start_time,
                error=f"Error: {str(e)}",
                metadata={}
            )

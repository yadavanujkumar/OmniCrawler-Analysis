"""
Anti-bot bypass utilities including proxy rotation and user-agent randomization.
"""
import random
from typing import List, Optional, Dict
from fake_useragent import UserAgent


class AntiBot:
    """Utilities for bypassing anti-bot measures."""
    
    def __init__(self, proxies: Optional[List[str]] = None, custom_user_agents: Optional[List[str]] = None):
        """
        Initialize anti-bot utilities.
        
        Args:
            proxies: List of proxy URLs (e.g., ['http://proxy1:8080', 'http://proxy2:8080'])
            custom_user_agents: List of custom user agent strings
        """
        self.proxies = proxies or []
        self.custom_user_agents = custom_user_agents or []
        self.ua = UserAgent()
        self.proxy_index = 0
    
    def get_random_user_agent(self) -> str:
        """Get a random user agent string."""
        if self.custom_user_agents:
            return random.choice(self.custom_user_agents)
        
        # Fallback to fake-useragent library
        try:
            return self.ua.random
        except Exception:
            # Default user agent if library fails
            return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """
        Get the next proxy in rotation.
        
        Returns:
            Dictionary with http and https proxy URLs, or None if no proxies configured
        """
        if not self.proxies:
            return None
        
        proxy_url = self.proxies[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def get_random_proxy(self) -> Optional[Dict[str, str]]:
        """
        Get a random proxy from the list.
        
        Returns:
            Dictionary with http and https proxy URLs, or None if no proxies configured
        """
        if not self.proxies:
            return None
        
        proxy_url = random.choice(self.proxies)
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def get_headers(self) -> Dict[str, str]:
        """
        Get randomized HTTP headers.
        
        Returns:
            Dictionary of HTTP headers
        """
        return {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': random.choice([
                'en-US,en;q=0.9',
                'en-GB,en;q=0.9',
                'en-US,en;q=0.5',
            ]),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }


# Predefined user agent lists
CHROME_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

FIREFOX_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

SAFARI_USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
]

ALL_USER_AGENTS = CHROME_USER_AGENTS + FIREFOX_USER_AGENTS + SAFARI_USER_AGENTS

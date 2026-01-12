"""
Crawler package initialization.
"""
from .base_crawler import BaseCrawler, CrawlResult
from .lightweight_crawler import LightweightCrawler
from .browser_crawler import BrowserCrawler
from .ai_crawler import AICrawler

__all__ = [
    'BaseCrawler',
    'CrawlResult',
    'LightweightCrawler',
    'BrowserCrawler',
    'AICrawler'
]

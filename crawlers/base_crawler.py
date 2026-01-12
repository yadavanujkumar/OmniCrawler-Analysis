"""
Base crawler interface for all crawler implementations.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time


@dataclass
class CrawlResult:
    """Result of a crawl operation."""
    url: str
    success: bool
    time_taken: float
    status_code: Optional[int]
    content: Optional[str]
    error: Optional[str]
    data_size: int
    crawler_type: str
    metadata: Dict[str, Any]
    
    def has_data_integrity_issues(self) -> bool:
        """Check if the result has data integrity issues."""
        if not self.success:
            return True
        if self.status_code and self.status_code in [403, 429, 503]:
            return True
        if not self.content or len(self.content.strip()) < 100:
            return True
        if "blocked" in self.content.lower()[:500] or "captcha" in self.content.lower()[:500]:
            return True
        return False
    
    def get_structural_quality_score(self) -> float:
        """
        Calculate structural quality score (0-100).
        Higher score means better structured content.
        """
        if not self.success or not self.content:
            return 0.0
        
        score = 50.0  # Base score
        
        # Check for structured data indicators
        if self.metadata.get('has_json', False):
            score += 20
        if self.metadata.get('has_markdown', False):
            score += 15
        if self.metadata.get('clean_text', False):
            score += 15
        
        # Penalize raw HTML
        if '<html' in self.content[:100].lower():
            score -= 10
        
        return min(100.0, max(0.0, score))


class BaseCrawler(ABC):
    """Base class for all crawlers."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def crawl(self, url: str, **kwargs) -> CrawlResult:
        """
        Crawl a URL and return the result.
        
        Args:
            url: The URL to crawl
            **kwargs: Additional crawler-specific parameters
            
        Returns:
            CrawlResult object with crawl information
        """
        pass
    
    def _create_result(
        self,
        url: str,
        success: bool,
        start_time: float,
        status_code: Optional[int] = None,
        content: Optional[str] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CrawlResult:
        """Helper method to create a CrawlResult."""
        time_taken = time.time() - start_time
        data_size = len(content) if content else 0
        
        return CrawlResult(
            url=url,
            success=success,
            time_taken=time_taken,
            status_code=status_code,
            content=content,
            error=error,
            data_size=data_size,
            crawler_type=self.name,
            metadata=metadata or {}
        )

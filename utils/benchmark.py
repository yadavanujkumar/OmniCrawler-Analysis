"""
Benchmarking engine to track and compare crawler performance metrics.
"""
from typing import List, Dict, Any
import pandas as pd
from crawlers.base_crawler import CrawlResult


class BenchmarkEngine:
    """Engine for benchmarking and comparing crawler results."""
    
    def __init__(self):
        self.results: List[CrawlResult] = []
    
    def add_result(self, result: CrawlResult):
        """Add a crawl result to the benchmark."""
        self.results.append(result)
    
    def clear_results(self):
        """Clear all stored results."""
        self.results = []
    
    def get_comparison_table(self) -> pd.DataFrame:
        """
        Generate a comparison table of all crawler results.
        
        Returns:
            DataFrame with comparison metrics
        """
        if not self.results:
            return pd.DataFrame()
        
        data = []
        for result in self.results:
            data.append({
                'Crawler': result.crawler_type,
                'Success': '✓' if result.success else '✗',
                'Time (s)': f"{result.time_taken:.2f}",
                'Status Code': result.status_code or 'N/A',
                'Data Size (KB)': f"{result.data_size / 1024:.2f}",
                'Data Integrity': '✓' if not result.has_data_integrity_issues() else '✗',
                'Quality Score': f"{result.get_structural_quality_score():.1f}",
                'Error': result.error if result.error else '-'
            })
        
        return pd.DataFrame(data)
    
    def get_winner(self) -> Dict[str, Any]:
        """
        Determine the winner based on multiple criteria.
        
        Returns:
            Dictionary with winner information and reasoning
        """
        if not self.results:
            return {'winner': None, 'reason': 'No results available'}
        
        successful_results = [r for r in self.results if r.success]
        
        if not successful_results:
            return {'winner': None, 'reason': 'All crawlers failed'}
        
        # Calculate scores for each crawler
        scores = {}
        for result in successful_results:
            crawler = result.crawler_type
            score = 0
            
            # Speed score (inverse of time, normalized)
            if result.time_taken > 0:
                speed_score = 1 / result.time_taken * 10
                score += min(speed_score, 30)  # Max 30 points
            
            # Data integrity score
            if not result.has_data_integrity_issues():
                score += 30
            
            # Quality score
            score += result.get_structural_quality_score() * 0.4  # Max 40 points
            
            scores[crawler] = score
        
        # Find winner
        winner = max(scores.items(), key=lambda x: x[1])
        
        # Generate reasoning
        winner_result = next(r for r in self.results if r.crawler_type == winner[0])
        
        reasoning_parts = []
        reasoning_parts.append(f"Completed in {winner_result.time_taken:.2f}s")
        
        if not winner_result.has_data_integrity_issues():
            reasoning_parts.append("excellent data integrity")
        
        quality = winner_result.get_structural_quality_score()
        if quality >= 80:
            reasoning_parts.append(f"high structural quality ({quality:.0f}/100)")
        
        reasoning = f"{winner[0]} won with a score of {winner[1]:.1f}/100. " + ", ".join(reasoning_parts)
        
        return {
            'winner': winner[0],
            'score': winner[1],
            'reason': reasoning,
            'all_scores': scores
        }
    
    def get_cost_benefit_analysis(self) -> pd.DataFrame:
        """
        Generate a cost-benefit analysis comparing crawlers.
        
        Returns:
            DataFrame with cost-benefit metrics
        """
        if not self.results:
            return pd.DataFrame()
        
        data = []
        
        # Define relative costs (arbitrary units)
        costs = {
            'Lightweight': 1,      # Cheapest
            'Browser-Based': 5,    # More expensive (browser overhead)
            'AI-Agentic': 10       # Most expensive (API costs)
        }
        
        for result in self.results:
            crawler = result.crawler_type
            cost = costs.get(crawler, 5)
            
            # Calculate benefit score
            benefit = 0
            if result.success:
                benefit += 40
                if not result.has_data_integrity_issues():
                    benefit += 30
                benefit += result.get_structural_quality_score() * 0.3
            
            # Calculate cost-benefit ratio
            cb_ratio = benefit / cost if cost > 0 else 0
            
            data.append({
                'Crawler': crawler,
                'Relative Cost': cost,
                'Benefit Score': f"{benefit:.1f}",
                'Cost-Benefit Ratio': f"{cb_ratio:.2f}",
                'Speed Rank': '',
                'Quality Rank': '',
                'Recommendation': ''
            })
        
        df = pd.DataFrame(data)
        
        # Add rankings
        if len(self.results) > 0:
            successful_times = [(r.crawler_type, r.time_taken) for r in self.results if r.success]
            if successful_times:
                sorted_by_speed = sorted(successful_times, key=lambda x: x[1])
                speed_ranks = {crawler: idx + 1 for idx, (crawler, _) in enumerate(sorted_by_speed)}
                df['Speed Rank'] = df['Crawler'].map(lambda x: speed_ranks.get(x, '-'))
            
            quality_scores = [(r.crawler_type, r.get_structural_quality_score()) for r in self.results if r.success]
            if quality_scores:
                sorted_by_quality = sorted(quality_scores, key=lambda x: x[1], reverse=True)
                quality_ranks = {crawler: idx + 1 for idx, (crawler, _) in enumerate(sorted_by_quality)}
                df['Quality Rank'] = df['Crawler'].map(lambda x: quality_ranks.get(x, '-'))
        
        # Add recommendations
        def get_recommendation(row):
            cb = float(row['Cost-Benefit Ratio'])
            if cb > 5:
                return '🌟 Excellent'
            elif cb > 3:
                return '✓ Good'
            elif cb > 1:
                return '○ Fair'
            else:
                return '✗ Poor'
        
        df['Recommendation'] = df.apply(get_recommendation, axis=1)
        
        return df
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for all crawlers."""
        if not self.results:
            return {}
        
        return {
            'total_crawls': len(self.results),
            'successful_crawls': sum(1 for r in self.results if r.success),
            'avg_time': sum(r.time_taken for r in self.results) / len(self.results),
            'total_data_size': sum(r.data_size for r in self.results),
            'crawlers_tested': list(set(r.crawler_type for r in self.results))
        }

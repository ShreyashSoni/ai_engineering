"""Enhanced web scraping service for the Company Brochure Generator."""

import time
from typing import Optional
from bs4 import BeautifulSoup
import requests

from config import Config


class ScraperService:
    """Service for scraping website content and links with caching and retry logic."""
    
    def __init__(self):
        """Initialize the scraper service."""
        self.cache = {}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
    
    def _get_from_cache(self, url: str) -> Optional[tuple]:
        """
        Get content from cache if available and not expired.
        
        Args:
            url: The URL to check in cache
            
        Returns:
            Cached content tuple or None if not cached/expired
        """
        if url in self.cache:
            content, timestamp = self.cache[url]
            if time.time() - timestamp < Config.CACHE_TIMEOUT:
                return content
            else:
                # Remove expired cache entry
                del self.cache[url]
        return None
    
    def _add_to_cache(self, url: str, content: tuple):
        """
        Add content to cache with timestamp.
        
        Args:
            url: The URL to cache
            content: The content tuple to cache
        """
        self.cache[url] = (content, time.time())
    
    def _fetch_with_retry(self, url: str) -> Optional[requests.Response]:
        """
        Fetch URL with exponential backoff retry logic.
        
        Args:
            url: The URL to fetch
            
        Returns:
            Response object or None if all retries failed
        """
        for attempt in range(Config.MAX_RETRIES):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=Config.REQUEST_TIMEOUT
                )
                response.raise_for_status()
                return response
                
            except requests.exceptions.Timeout:
                if attempt < Config.MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise Exception(f"Timeout after {Config.MAX_RETRIES} attempts")
                
            except requests.exceptions.RequestException as e:
                if attempt < Config.MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise Exception(f"Failed to fetch URL: {str(e)}")
        
        return None
    
    def fetch_website_content_and_links(
        self,
        url: str,
        only_content: bool = False
    ) -> tuple[str, list[str]]:
        """
        Fetch website content and links in a single request.
        
        Args:
            url: The URL to scrape
            only_content: If True, only return content, skip link extraction
            
        Returns:
            Tuple of (content, links) where content is truncated text and links is list of URLs
        """
        # Check cache first
        cached = self._get_from_cache(url)
        if cached:
            return cached
        
        try:
            # Fetch the page
            response = self._fetch_with_retry(url)
            if not response:
                return "", []
            
            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract title
            title = soup.title.string if soup.title else "No title found"
            if title is None:
                title = "No title found"
            
            # Extract text content
            text = ""
            if soup.body:
                # Remove irrelevant elements
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                text = soup.body.get_text(separator="\n", strip=True)
            
            # Truncate content
            content = (title + "\n\n" + text)[:Config.MAX_CONTENT_LENGTH]
            
            # Extract links if needed
            links: list[str] = []
            if not only_content:
                all_links = [link.get("href") for link in soup.find_all("a")]
                # Filter out None and empty links, ensure they are strings
                links = [str(link) for link in all_links if link and isinstance(link, str)]
            
            result = (content, links)
            
            # Cache the result
            self._add_to_cache(url, result)
            
            return result
            
        except Exception as e:
            raise Exception(f"Error scraping {url}: {str(e)}")
    
    def fetch_multiple_pages(
        self,
        urls: list[str],
        max_length: Optional[int] = None
    ) -> str:
        """
        Fetch content from multiple pages and aggregate.
        
        Args:
            urls: List of URLs to fetch
            max_length: Maximum total length of aggregated content
            
        Returns:
            Aggregated content string
        """
        if max_length is None:
            max_length = Config.MAX_AGGREGATED_CONTENT
        
        aggregated = ""
        
        for url in urls:
            if len(aggregated) >= max_length:
                break
            
            try:
                content, _ = self.fetch_website_content_and_links(url, only_content=True)
                remaining = max_length - len(aggregated)
                aggregated += content[:remaining] + "\n\n"
            except Exception as e:
                # Log error but continue with other URLs
                print(f"Warning: Failed to fetch {url}: {str(e)}")
                continue
        
        return aggregated.strip()
    
    def clear_cache(self):
        """Clear all cached content."""
        self.cache.clear()
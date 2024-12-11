import os
import json
import logging
import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import concurrent.futures
import time
import random

class WebScraper:
    def __init__(self, 
                 user_agent: str = 'SportPropPredictor/1.0',
                 max_retries: int = 3,
                 retry_delay: int = 2):
        """
        Initialize web scraper with configurable settings.
        
        Args:
            user_agent (str): Custom user agent for requests
            max_retries (int): Maximum number of retry attempts
            retry_delay (int): Delay between retry attempts
        """
        self.user_agent = user_agent
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Setup logging
        self.logger = logging.getLogger('WebScraper')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Ensure data storage directory exists
        self.data_dir = os.path.join('data', 'web_scraping')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Default headers
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }

    def _get_session(self) -> requests.Session:
        """
        Create a configured requests session.
        
        Returns:
            requests.Session: Configured session object
        """
        session = requests.Session()
        session.headers.update(self.headers)
        return session

    def scrape_url(self, url: str, parser: str = 'html.parser') -> Dict[str, Any]:
        """
        Scrape a single URL with retry mechanism.
        
        Args:
            url (str): URL to scrape
            parser (str): BeautifulSoup parser to use
        
        Returns:
            Dict with scraping results
        """
        for attempt in range(self.max_retries):
            try:
                session = self._get_session()
                response = session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, parser)
                
                # Store raw HTML
                self._save_raw_html(url, response.text)
                
                return {
                    'url': url,
                    'status_code': response.status_code,
                    'content_length': len(response.text),
                    'parsed_content': self._extract_content(soup)
                }
            
            except requests.RequestException as e:
                self.logger.warning(f"Scraping attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (2 ** attempt) + random.random())
                else:
                    self.logger.error(f"Failed to scrape {url} after {self.max_retries} attempts")
                    return {}

    def _extract_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract structured content from BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
        
        Returns:
            Dict with extracted content
        """
        try:
            # Example content extraction (customize based on specific sports sites)
            return {
                'title': soup.title.string if soup.title else None,
                'headings': [h.text for h in soup.find_all(['h1', 'h2', 'h3'])],
                'paragraphs': [p.text for p in soup.find_all('p')],
                'links': [
                    {
                        'text': link.text.strip(),
                        'href': link.get('href')
                    } for link in soup.find_all('a') if link.get('href')
                ]
            }
        except Exception as e:
            self.logger.error(f"Content extraction error: {e}")
            return {}

    def scrape_multiple_urls(self, urls: List[str], max_workers: int = 5) -> List[Dict[str, Any]]:
        """
        Scrape multiple URLs concurrently.
        
        Args:
            urls (List[str]): List of URLs to scrape
            max_workers (int): Maximum number of concurrent workers
        
        Returns:
            List of scraping results
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit scraping tasks
            future_to_url = {
                executor.submit(self.scrape_url, url): url for url in urls
            }
            
            results = []
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Exception scraping {url}: {e}")
        
        return results

    def _save_raw_html(self, url: str, content: str):
        """
        Save raw HTML content to a file.
        
        Args:
            url (str): Source URL
            content (str): HTML content
        """
        filename = f"{url.replace('://', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"Saved raw HTML for {url} to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving HTML: {e}")

def main():
    """
    Example usage of WebScraper
    """
    # Sports-related websites to scrape (example URLs)
    sports_urls = [
        'https://www.espn.com/nba/',
        'https://www.nfl.com/news/',
        'https://www.mlb.com/news'
    ]
    
    scraper = WebScraper()
    
    # Scrape multiple sports news sites
    results = scraper.scrape_multiple_urls(sports_urls)
    
    # Print summary of scraping results
    for result in results:
        print(f"URL: {result.get('url')}")
        print(f"Status Code: {result.get('status_code')}")
        print(f"Content Length: {result.get('content_length')}")
        print("-" * 50)

if __name__ == "__main__":
    main()
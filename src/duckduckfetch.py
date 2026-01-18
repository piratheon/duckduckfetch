import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import json
import random
import time
import os
from typing import List, Dict, Optional, Any

class DuckDuckFetch:
    """Enhanced client for DuckDuckGo HTML search API with proxy support"""
    
    BASE_URL = "https://duckduckgo.com/lite/"
    
    def __init__(self, proxy_file: Optional[str] = None):
        """Initialize with browser-like headers and optional proxy chain"""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://duckduckgo.com/",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://html.duckduckgo.com"
        })
        
        # Load proxies if file is provided
        self.proxies = []
        self.current_proxy_index = 0
        if proxy_file and os.path.exists(proxy_file):
            self._load_proxies(proxy_file)
    
    def _load_proxies(self, proxy_file: str):
        """Load proxies from a file, one proxy per line in format: [protocol://]host:port"""
        try:
            with open(proxy_file, 'r') as f:
                for line in f:
                    proxy = line.strip()
                    if proxy and not proxy.startswith('#'):  # Skip empty lines and comments
                        # Ensure proxy has a protocol
                        if not proxy.startswith(('http://', 'https://', 'socks5://')):
                            proxy = 'http://' + proxy
                        self.proxies.append(proxy)
            print(f"Loaded {len(self.proxies)} proxies from {proxy_file}")
        except Exception as e:
            print(f"Error loading proxies from {proxy_file}: {e}")
    
    def _get_proxy(self) -> Optional[Dict[str, str]]:
        """Get the next proxy in the chain"""
        if not self.proxies:
            return None
        
        proxy_url = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        
        # Format for requests
        if proxy_url.startswith('socks5://'):
            return {'http': proxy_url, 'https': proxy_url}
        else:
            return {'http': proxy_url, 'https': proxy_url}
    
    def _parse_results(self, html: str, max_results: int) -> List[Dict[str, str]]:
        """Parse HTML results into structured data"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # Find all result containers
        for result in soup.find_all('tr'):
            if len(results) >= max_results:
                break
            
            # Extract title and URL
            title_elem = result.find('a', class_='result-link')
            if not title_elem:
                continue
                
            title = title_elem.get_text(strip=True)
            url = title_elem.get('href', '').strip()
            
            # Extract snippet/description
            snippet_elem = result.find('td', class_='result-snippet')
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
            
            # Skip invalid results
            if not title or not url:
                continue
                
            results.append({
                'title': title,
                'url': url,
                'snippet': snippet
            })
        
        return results
    
    def search_json(self, query: str, region: Optional[str] = None, 
                    time_filter: Optional[str] = None, max_results: int = 10) -> str:
        """Perform search and return results as JSON string"""
        results = self.search(query, region, time_filter, max_results)
        return json.dumps(results, indent=2)
    
    def search_text(self, query: str, region: Optional[str] = None, 
                    time_filter: Optional[str] = None, max_results: int = 10) -> str:
        """Perform search and return results as formatted text"""
        results = self.search(query, region, time_filter, max_results)
        
        output = []
        for i, result in enumerate(results, 1):
            output.append(f"{i}. {result['title']}")
            output.append(f"   URL: {result['url']}")
            output.append(f"   Snippet: {result['snippet']}")
            output.append("")  # Empty line between results
        
        return "\n".join(output)

    def search(self, query: str, region: Optional[str] = None, 
               time_filter: Optional[str] = None, max_results: int = 10,
               retries: int = 3) -> List[Dict[str, str]]:
        """
        Perform search and return results
        
        Args:
            query (str): Search query
            region (str, optional): Region code (e.g., "us-en", "uk-en")
            time_filter (str, optional): Time filter ("d"=day, "w"=week, "m"=month, "y"=year)
            max_results (int, optional): Maximum results to return
            retries (int, optional): Number of retry attempts with different proxies
        
        Returns:
            list: List of dictionaries containing title, url, and snippet
        """
        params = {
            'q': query,
        }
        
        # Add optional parameters if provided
        if region:
            params['kl'] = region
        if time_filter:
            params['df'] = time_filter

        # Try with different proxies if needed
        last_exception = None
        for attempt in range(retries):
            try:
                proxy = self._get_proxy() if self.proxies else None
                
                response = self.session.get(
                    self.BASE_URL,
                    params=params,
                    proxies=proxy,
                    timeout=15
                )
                response.raise_for_status()
                return self._parse_results(response.text, max_results)
            
            except Exception as e:
                last_exception = e
                print(f"Attempt {attempt + 1} failed: {e}")
                # Wait before retrying
                time.sleep(random.uniform(1, 3))
        
        # If all retries failed
        raise Exception(f"All {retries} attempts failed. Last error: {last_exception}")
    
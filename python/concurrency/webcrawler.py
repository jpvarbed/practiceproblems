# pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading
import time

class WebCrawler:
    def __init__(self, start_url, max_depth=3, max_threads=10):
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_threads = max_threads
        self.queue = Queue()
        self.visited = set()
        self.lock = threading.Lock()

    def crawl(self):
        self.queue.put((self.start_url, 0))
        # reuse threads from the pool
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            while not self.queue.empty():
                url, depth = self.queue.get()
                if depth > self.max_depth:
                    continue
                
                if url not in self.visited:
                    executor.submit(self.fetch_url, url, depth)

    def fetch_url(self, url, depth):
        with self.lock:
            if url in self.visited:
                return
            self.visited.add(url)
        
        try:
            response = requests.get(url, timeout=5)
            print(f"Crawled: {url} (depth: {depth})")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                self.parse_links(soup, url, depth)
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")

    def parse_links(self, soup, base_url, depth):
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            if self.is_valid_url(full_url):
                with self.lock:
                    if full_url not in self.visited:
                        self.queue.put((full_url, depth + 1))

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

if __name__ == "__main__":
    start_url = "http://example.com"  # Replace with your desired starting URL
    crawler = WebCrawler(start_url, max_depth=3, max_threads=10)
    
    start_time = time.time()
    crawler.crawl()
    end_time = time.time()
    
    print(f"Crawling completed in {end_time - start_time:.2f} seconds")
    print(f"Total URLs visited: {len(crawler.visited)}")
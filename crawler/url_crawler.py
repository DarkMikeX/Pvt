import requests
from urllib.parse import urljoin, urlparse
import logging
import time
import re

logger = logging.getLogger(__name__)

class RecursiveCrawler:
    def __init__(self, max_depth=3, delay=1):
        """
        max_depth: Maximum depth for recursion
        delay: Seconds delay between requests to avoid overload
        """
        self.visited = set()
        self.max_depth = max_depth
        self.delay = delay  # polite crawling delay

    def crawl(self, url, depth=0):
        """
        Recursively crawl URLs up to max_depth, staying within the same domain.
        Returns a list of discovered unique URLs.
        """
        if depth > self.max_depth:
            return []

        if url in self.visited:
            return []

        self.visited.add(url)
        logger.info(f"Crawling URL: {url} at depth {depth}")

        urls_found = [url]

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Non-200 status code {response.status_code} for {url}")
                return urls_found
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return urls_found

        links = self._extract_links(response.text, url)
        for link in links:
            if link not in self.visited:
                time.sleep(self.delay)
                urls_found.extend(self.crawl(link, depth + 1))

        return urls_found

    def _extract_links(self, html, base_url):
        """
        Extract all href links within same domain from HTML content.
        """
        hrefs = re.findall(r'href=["\']?([^"\' >]+)', html)
        urls = []
        base_domain = urlparse(base_url).netloc

        for href in hrefs:
            absolute_url = urljoin(base_url, href)
            parsed = urlparse(absolute_url)
            if parsed.scheme in ['http', 'https'] and parsed.netloc == base_domain:
                urls.append(absolute_url)
        return urls


# Example usage:
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     crawler = RecursiveCrawler(max_depth=3, delay=1)
#     found_urls = crawler.crawl("https://example.com")
#     print(f"Discovered URLs ({len(found_urls)}):")
#     for u in found_urls:
#         print(u)

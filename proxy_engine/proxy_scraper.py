import requests
import threading
import time
import random
import logging

logger = logging.getLogger(__name__)

class ProxyEngine:
    def __init__(self, proxy_sources, validate_url="http://httpbin.org/ip", thread_count=10):
        """
        proxy_sources: list of URLs returning proxy lists (http, socks4, socks5)
        validate_url: URL to validate proxies
        thread_count: concurrency for fetching/validating
        """
        self.proxy_sources = proxy_sources
        self.validate_url = validate_url
        self.thread_count = thread_count
        self.valid_proxies = []
        self.lock = threading.Lock()

    def scrape_proxies(self):
        """
        Scrape all proxy sources to collect raw proxy list
        """
        proxies = []
        for url in self.proxy_sources:
            try:
                logger.info(f"Fetching proxies from {url}")
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    raw_list = resp.text.splitlines()
                    proxies.extend(raw_list)
                else:
                    logger.warning(f"Failed to fetch proxies from {url}, status: {resp.status_code}")
            except Exception as e:
                logger.error(f"Exception fetching {url}: {e}")
        logger.info(f"Scraped {len(proxies)} proxies in total")
        return proxies

    def validate_proxy(self, proxy):
        """
        Validate a single proxy by making a request to validate_url
        """
        protocols = ["http", "https", "socks4", "socks5"]
        for protocol in protocols:
            proxy_url = f"{protocol}://{proxy}"
            try:
                resp = requests.get(self.validate_url, proxies={protocol: proxy_url}, timeout=5)
                if resp.status_code == 200:
                    with self.lock:
                        self.valid_proxies.append((protocol, proxy))
                    logger.info(f"Valid proxy: {proxy_url}")
                    return
            except Exception:
                continue

    def validate_proxies(self, proxies):
        """
        Concurrently validate all proxies gathered
        """
        threads = []
        for proxy in proxies:
            t = threading.Thread(target=self.validate_proxy, args=(proxy,))
            t.start()
            threads.append(t)
            if len(threads) >= self.thread_count:
                for thr in threads:
                    thr.join()
                threads = []

        # Join remaining threads
        for thr in threads:
            thr.join()

        logger.info(f"Validated {len(self.valid_proxies)} proxies")

    def get_proxy(self):
        """
        Get a random valid proxy formatted for requests library usage
        Returns dict like {"http": "http://ip:port", "https": "http://ip:port"}
        """
        if not self.valid_proxies:
            logger.warning("No valid proxies available")
            return None
        protocol, proxy = random.choice(self.valid_proxies)
        proxy_url = f"{protocol}://{proxy}"
        if protocol in ["socks4", "socks5"]:
            # Requests expects socks proxy URLs explicitly
            proxies = {"http": proxy_url, "https": proxy_url}
        else:
            proxies = {"http": proxy_url, "https": proxy_url}
        return proxies

    def refresh_proxies(self):
        """
        Full scrape + validate cycle to refresh proxy pool
        """
        logger.info("Starting proxy refresh cycle")
        raw_proxies = self.scrape_proxies()
        self.valid_proxies = []
        self.validate_proxies(raw_proxies)
        logger.info("Proxy refresh completed")

# Example proxy sources
PROXY_SOURCES = [
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5"
]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    proxy_engine = ProxyEngine(PROXY_SOURCES)
    proxy_engine.refresh_proxies()
    print(f"Valid proxies: {proxy_engine.valid_proxies}")
    print("Random proxy dict for use in requests:", proxy_engine.get_proxy())

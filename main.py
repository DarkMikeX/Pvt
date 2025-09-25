import logging
import asyncio

from bot.telegram_bot import main as telegram_bot_main
from exploit.exploits import Exploits
from recon.recon_crawler import ReconCrawler
from crawler.url_crawler import RecursiveCrawler
from proxy_engine.proxy_scraper import ProxyEngine
from notifier.notifier import Notifier
from ai_logic.logic_planner import LogicPlanner
import config

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def setup_bot_environment():
    # Initialize core modules with config paths
    exploits = Exploits(config.TOOL_PATHS)
    recon = ReconCrawler(config.TOOL_PATHS)
    crawler = RecursiveCrawler(max_depth=3)
    proxy_engine = ProxyEngine([
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://www.proxy-list.download/api/v1/get?type=socks4",
        "https://www.proxy-list.download/api/v1/get?type=socks5"
    ])
    notifier = Notifier()
    logic_planner = LogicPlanner()

    # Refresh proxies initially (can be repeated periodically)
    proxy_engine.refresh_proxies()

    # You might want to pass these module instances somewhere
    # For simplicity, we just start the Telegram bot now
    telegram_bot_main()


def main():
    logging.info("Starting Pentest Bot environment...")
    asyncio.run(setup_bot_environment())

if __name__ == "__main__":
    main()

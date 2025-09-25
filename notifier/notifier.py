import logging
from telegram import Bot
import config
import asyncio

logger = logging.getLogger(__name__)

class Notifier:
    def __init__(self):
        self.bot = Bot(token=config.TELEGRAM_TOKEN)
        self.admins = config.ADMINS

    async def notify_admins(self, message):
        """
        Send a message string to all admin Telegram users asynchronously.
        """
        coros = []
        for admin_id in self.admins:
            coros.append(self._send_message(admin_id, message))
        await asyncio.gather(*coros)

    async def _send_message(self, chat_id, text):
        try:
            await self.bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
            logger.info(f"Notification sent to admin {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send notification to admin {chat_id}: {e}")

    async def notify_hit(self, details):
        msg = f"🎯 *Hit Detected!* \n{details}"
        await self.notify_admins(msg)

    async def notify_dump(self, details):
        msg = f"💾 *Data Dumped:* \n{details}"
        await self.notify_admins(msg)

    async def notify_shell(self, details):
        msg = f"🐚 *Shell Activated:* \n{details}"
        await self.notify_admins(msg)

    async def notify_panel(self, details):
        msg = f"🔓 *Panel Found:* \n{details}"
        await self.notify_admins(msg)

import asyncio

from telethon import TelegramClient

from src.domain.interfaces import AbstractTelegramClient
from src.config import settings


class TgClient(AbstractTelegramClient): 
    def __init__(self): 
        self.client = TelegramClient(fr"{settings.SESSION_PATH}\{settings.SESSION_NAME}.session", settings.API_ID, settings.API_HASH)
        self.client.start()

    def send_forecast_to_group(self, forecast: str) -> None:
        loop = asyncio.get_event_loop() 
        if loop.is_running():
            loop.create_task(self._send_forecast(forecast))
        else:
            loop.run_until_complete(self._send_forecast(forecast))

    async def _send_forecast(self, forecast: str) -> None: 
        entity = await self.client.get_entity(settings.GROUP_LINK)
        await self.client.send_message(entity=entity, message=forecast)

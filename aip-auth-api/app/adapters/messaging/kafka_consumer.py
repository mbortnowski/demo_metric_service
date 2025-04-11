from aiokafka import AIOKafkaConsumer
import json
import asyncio
from typing import Callable, Awaitable, Dict, Any
from app.ports.messaging.kafka_consumer import KafkaConsumerPort
from app.config.models import KafkaSettings

class KafkaConsumerAdapter(KafkaConsumerPort):
    def __init__(self, settings: KafkaSettings):
        self.settings = settings
        self.consumer = AIOKafkaConsumer(
            settings.consumer_topic,
            bootstrap_servers=settings.bootstrap_servers,
            group_id=settings.consumer_group,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.running = False
        self.task = None
    
    async def start(self) -> None:
        await self.consumer.start()
        self.running = True
    
    async def stop(self) -> None:
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        await self.consumer.stop()
    
    async def _consume(self, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        try:
            async for msg in self.consumer:
                if not self.running:
                    break
                await callback(msg.value)
        except asyncio.CancelledError:
            pass
    
    async def subscribe(self, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        if self.task:
            return
        
        self.task = asyncio.create_task(self._consume(callback))
